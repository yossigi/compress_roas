import netaddr
import map_functions
from pytrie import SortedStringTrie as trie

class IPPrefix:
    """
This class represents a single IP prefix within a ROA. It is a prefix and a maxlength limit.
    """
    def __init__(self, prefix, maxlen):
        """
        Init from prefix and maxlen
        """
        self.prefix = netaddr.IPNetwork(prefix)
        self.maxlen = maxlen

    def covers(self, ip_prefix):
        """ returns whether this IP prefix covers the given prefix (and therefore that prefix is either valid or invalid) """
        return (ip_prefix in self.prefix)

    def match_length(self, ip_prefix):
        """ returns whether the length of a given prefix is allowed by the maxlength limit of this prefix """
        return (ip_prefix.prefixlen <= self.maxlen)


# The following describes the three statuses that a prefix may have in the RPKI
ROA_STATUS_UNKNOWN = 0
ROA_STATUS_VALID = 1
ROA_STATUS_INVALID = 2

class ROA:
    """
This class represents a ROA, it may map multiple prefixes to one ASN.
    """
    def __init__(self, asn, prefixes):
        """
        Initialization from ASN and a list of prefixes in tuples of (prefix, maxlen)
        """
        self.asn = int(asn)
        self.prefixes = []
        for prefix, maxlen in prefixes:
            net = IPPrefix(prefix, int(maxlen))
            # make sure the prefix is either IPv4 or IPv6
            if ((net.prefix.version == 4) or (net.prefix.version == 6)):
                # append the new IPPrefix object to this ROA
                self.prefixes.append(net)

    def get_covering_prefixes(self, ip_prefix):
        """
        returns all IPPrefixes in this ROA that cover the given ip_prefix
        """
        covering_prefixes = set()
        for roa_prefix in self.prefixes:
            if roa_prefix.covers(ip_prefix):
                covering_prefixes.add(roa_prefix)
        return covering_prefixes

    def covers(self, ip_prefix):
        """
        Returns whether the given ip_prefix is covered by this ROA
        """
        return len(self.get_covering_prefixes(ip_prefix)) > 0

    def get_status(self, asn, prefix):
        """
        Returns the status of the given prefix announced by asn given this ROA.
        """
        covering_prefixes_in_roa = self.get_covering_prefixes(prefix)

        # this ROA doesn't cover this prefix, so status is unknown (only concerning this ROA)
        if len(covering_prefixes_in_roa) == 0:
            return ROA_STATUS_UNKNOWN

        # ASN mismatch, this prefix is invalid (unless some other ROA permits this announcement)
        if self.asn != asn:
            return ROA_STATUS_INVALID

        # some prefix in this ROA allows the advertised prefix length, so announcement (asn, prefix) is valid
        for roa_prefix in covering_prefixes_in_roa:
            if roa_prefix.match_length(prefix):
                return ROA_STATUS_VALID

        # prefix is covered, but not valid, so it is invalid (unless some other ROA permits this announcement)
        return ROA_STATUS_INVALID


class ROATree:
    """
Aggregates and indexes all ROAs so they are easy to search.
    """
    def __init__(self, roas_file):
        """
        Parse the ROA file as provided by the RPKI tool chain.
        """
        all_roas = {}
        with open(roas_file, "r") as f:
            # each line represents a ROA, iterate through the lines.
            for line in f:
                line = line.replace("\n","")
                splitted = line.split(" ")
                # parse out the ASN and prefixes in this ROA
                asn = splitted[1]
                prefixes = []
                for prefix in splitted[2:]:
                    maxlen = 0
                    if "-" in prefix:
                        prefix, maxlen = prefix.split("-")
                    else:
                        maxlen = netaddr.IPNetwork(prefix).prefixlen
                    prefixes.append((prefix, maxlen))
                    k = map_functions.prefix_to_key(netaddr.IPNetwork(prefix))
                    if k not in all_roas:
                        all_roas[k] = []
                    all_roas[k].append(ROA(asn, prefixes))
        # arrange all prefixes in the ROAs in a trie, so they are easy to search.
        self.all_roas = trie(**all_roas)

    def is_valid(self, prefix, asn):
        """
        Returns whether the announcement (ASN, prefix) is valid by the RPKI
        """
        adv = map_functions.prefix_to_key(prefix)
        try:
            # iterate through all covering ROAs
            while (len(adv) > 1):
                ancestor = self.all_roas.longest_prefix(adv)
                for roa in self.all_roas[ancestor]:
                    # for each covering ROA, test if it allows this advertisement
                    if (roa.get_status(asn, prefix) == ROA_STATUS_VALID):
                        return True
                adv = ancestor[:-1]
        except KeyError:
            pass
        return False

def save_valid_announcements_to_file(bgp_announcements_file, roas_file, output_file = "bgp_valid_announcements.txt"):
    """
    Create a file containing all prefixes that are announced in BGP (given in bgp_announcements_file)
    and are valid by the ROAs in the RPKI (given in roas_file). It saves the valid prefixes in output_file.
    """

    # parse the ROAs
    roas = ROATree(roas_file)

    with open(output_file, "w") as outf:
        with open(bgp_announcements_file, "r") as f:
            # iterate through the lines in the file, each line corresponds to a BGP advertisement
            for line in f:
                # parse each advertisement
                line = line.replace("\n","")
                prefix, asn = line.split(",")
                prefix, ml = prefix.split("-")

                # if it is valid, write it to file
                if roas.is_valid(netaddr.IPNetwork(prefix), int(asn)):
                    outf.write(line + "\n")
    return output_file
