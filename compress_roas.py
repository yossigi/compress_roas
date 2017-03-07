# -*- coding: utf-8 -

from pytrie import NULL, SortedStringTrie as Trie
from valid_announcements import save_valid_announcements_to_file
import map_functions as mf
import netaddr
import os
import sys
import time
import subprocess


def parseROAs(roaDumpPath, outputFilename='roa_list.txt'):
    '''
        Given a ROAs rcynic dump, this function uses 'scan_roas' tool from 'rpki.net' (included in this repository)
        to parse the ROAs in the directory and creates an ouput file with each ROA as an one line.
    '''
    outputFilename = 'Data/parsedData/' + outputFilename
    terminal = subprocess.Popen(
        ['tools/scan_roas', os.path.abspath(roaDumpPath)], stdout=subprocess.PIPE)
    output = terminal.communicate()[0]
    open(outputFilename, 'w').write(output)
    return outputFilename


def parseBGPs(BGPDumpPath, outputFilename='bgp_announcements.txt'):
    '''
        Given a BGP RIB Dump, this function uses the parser tool 'bgp_announcement_parser' included in the repository
        to create an ouput file that contains all the BGP announcements.
    '''
    outputFilename = 'Data/parsedData/' + outputFilename
    terminal = subprocess.call(
        ['./tools/bgp_announcement_parser', os.path.abspath(BGPDumpPath), outputFilename], stdout=subprocess.PIPE)
    return outputFilename


def getBGPs(filename):
    IPdict = dict()
    Trie_dict = {}
    prefix_count = 0
    BGPs = open(filename, 'r')
    for BGP in BGPs:
        prefix_count += 1
        line = BGP.replace("\n", "").split(',')
        AS = line[1]
        IP = line[0]
        ip = IP.split('-')
        prefix = ip[0]
        key = mf.prefix_to_key(netaddr.IPNetwork(prefix))
        prefixLength = len(key.split('$')[1])
        try:
            maxLength = int(ip[1])
            if maxLength < prefixLength:
                # To skip the prefix's in which the maxLength is less that the
                # prefix length.
                continue
        except IndexError:
            # In case the maxLength didn't exist.
            maxLength = netaddr.IPNetwork(prefix).prefixlen
        if AS in Trie_dict:
            if key in Trie_dict[AS]:
                Trie_dict[AS][key][2] = max(maxLength, Trie_dict[AS][key][2])
            else:
                Trie_dict[AS][key] = [AS, prefix, maxLength]
        else:
            Trie_dict[AS] = {key: [AS, prefix, maxLength]}

    print "# of prefix's before:", prefix_count
    return (Trie_dict, prefix_count)


def getROAs(filename):
    '''
    Takes a list of ROAs and then constructs a Trie of prefixes for each unique AS in the ROAs
    '''
    Trie_dict = {}
    count_roas = 0
    count_prefixs = 0
    count_AS = 0
    ROAs = open(filename, 'r')
    for roa in ROAs:
        count_roas += 1
        line = roa.replace("\n", "").split(' ')
        AS = line[1]
        IP = line[2:]
        for prefix in IP:
            ip = prefix.split('-')
            prefix_ip = ip[0]
            key = mf.prefix_to_key(netaddr.IPNetwork(prefix_ip))
            prefixLength = netaddr.IPNetwork(prefix_ip).prefixlen
            try:
                maxLength = int(ip[1])
                if maxLength < prefixLength:
                    # To skip the prefix's in which the maxLength is less that
                    # the prefix length.
                    continue
            except IndexError:
                # In case the maxLength didn't exist.
                maxLength = netaddr.IPNetwork(prefix_ip).prefixlen
            if AS in Trie_dict:
                if key in Trie_dict[AS]:
                    Trie_dict[AS][key][2] = max(
                        maxLength, Trie_dict[AS][key][2])
                else:
                    count_prefixs += 1
                    Trie_dict[AS][key] = [AS, prefix_ip, maxLength]
            else:
                count_AS += 1
                count_prefixs += 1
                Trie_dict[AS] = {key: [AS, prefix_ip, maxLength]}

    print "# of ROA's :", count_roas
    print "# of AS's :", count_AS
    print "# of prefix's before:", count_prefixs
    return (Trie_dict, count_prefixs)


def compress(AS, mDict):
    def final_compress(Trie):
        def compress_Tries(node):
            ''' This function compresses the prefix's '''
            if node is None or (not node.children):
                # When you reach a leaf node, just stop.
                return

            g = node.children.iteritems()

            # To get pointers on the children nodes.
            fchild = node.children.get(str(g.next()[0]))
            try:
                schild = node.children.get(str(g.next()[0]))
            # in case a second child doesn't exist.
            except StopIteration:
                schild = None

            # The recursive call to reach the end of the Trie.
            compress_Tries(fchild)
            compress_Tries(schild)

            # Check if the node is an prefix (not just a connecting node) and
            # that 2 children exist with prefix's and value's
            if node.value is not NULL and fchild.value is not NULL and schild is not None and schild.value is not NULL:
                # To check if the maxLength of the parent is higher or equal to
                # the max(children's  maxLength)
                if node.value[2] >= maxML([fchild, schild]):
                    pass  # No need to change the maxLength in this case.
                else:
                    # Only update the max length of the parent if it's less
                    # than the max of children
                    node.value[2] = minML([fchild, schild])
                # Only hide a child if the parent's max length is covering the child's max length
                # b_list = [node,fchild,schild]
                # print 'before:',b_list
                if node.value[2] >= fchild.value[2]:
                    key = mf.prefix_to_key(netaddr.IPNetwork(fchild.value[1]))
                    del Trie[key]
                    # del b_list[1]
                # Only hide a child if the parent's max length is covering the
                # child's max length
                if node.value[2] >= schild.value[2]:
                    key = mf.prefix_to_key(netaddr.IPNetwork(schild.value[1]))
                    del Trie[key]
                    # del b_list[-1]
                # print 'after:',b_list

        def minML(childList):
            ''' This method should return the min of the children's maxLength'''
            numlist = list()
            for child in childList:
                numlist += [child.value[2]]  # Add the MaxLength to the list
            return min(numlist)

        def maxML(childList):
            ''' This method should return the max of the children's maxLength'''
            numlist = list()
            for child in childList:
                numlist += [child.value[2]]  # Add the MaxLength to the list
            return max(numlist)

        compress_Tries(Trie._root)
        return dict(Trie)

    t = Trie(**mDict[AS])
    mDict[AS] = final_compress(t)


def testROA(roaDumpPath):
    roaDump = parseROAs(roaDumpPath)
    Trie_Dict, before = getROAs(roaDump)

    def compressAll():
        [compress(key, Trie_Dict) for key in Trie_Dict.keys()]

    # timers
    begin = time.time()
    compressAll()
    end = time.time()

    # This is another counter that does the same as 'before'.
    after = sum([len(Trie_Dict[key]) for key in Trie_Dict.keys()])

    diff = before - after
    p = float(diff / float(before)) * 100.0

    # Statistics
    print "# of prefix's after:", after
    print "compression rate:", p, '%'
    print "compression time:", end - begin, "seconds"


def testAllBGP(bgpDumpPath):
    bgpDump = parseBGPs(bgpDumpPath)

    Trie_Dict, before = getBGPs(bgpDump)

    def compressAll():
        [compress(key, Trie_Dict) for key in Trie_Dict.keys()]

    # timers
    begin = time.time()
    compressAll()
    end = time.time()

    # This is another counter that counts how many prefixes are in the Tries.
    after = sum([len(Trie_Dict[key]) for key in Trie_Dict.keys()])

    diff = before - after
    p = float(diff / float(before)) * 100.0

    # Statistics
    print "# of prefix's after:", after
    print "compression rate:", p, '%'
    print "compression time:", end - begin, "seconds"


def testValidBGP(bgpDumpPath, roaDumpPath):

    roaDump = parseROAs(roaDumpPath)
    bgpDump = parseBGPs(bgpDumpPath)
    validDump = save_valid_announcements_to_file(
        bgpDump, roaDump, 'Data/parsedData/' + 'bgp_valid_announcements.txt')

    Trie_Dict, before = getBGPs(validDump)

    def compressAll():
        [compress(key, Trie_Dict) for key in Trie_Dict.keys()]

    # timers
    begin = time.time()
    compressAll()
    end = time.time()

    # This is another counter that does the same as 'before'.
    after = sum([len(Trie_Dict[key]) for key in Trie_Dict.keys()])

    diff = before - after
    p = float(diff / float(before)) * 100.0

    # Statistics
    print "# of prefix's after:", after
    print "compression rate:", p, '%'
    print "compression time:", end - begin, "seconds"

ROADumpPath, BGPDumpPath = sys.argv[1:3]

testROA(ROADumpPath)
print '------'
testAllBGP(BGPDumpPath)
print '------'
testValidBGP(BGPDumpPath, ROADumpPath)
