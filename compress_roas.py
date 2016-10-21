# -*- coding: utf-8 -

from pytrie import NULL,SortedStringTrie as Trie
import netaddr
from multiprocessing import Process, Manager, Pool,cpu_count
import time

def getDictCSV(filename):
    IPdict = dict()
    Trie_dict = {}
    # rip = 0
    file = open(filename, 'r')
    for line in file:
        # rip += 1
        line = line[:-1].split(',')
        AS = line[1][:-1]
        IP = line[0]
        Time = ''
        ip = IP.split('-')
        prefix = ip[0]
        key = prefix_to_key(prefix)
        prefixLength = len(key.split('$')[1])
        # if int(key[0]) == 4:
        #     maxLength = 32
        # elif int(key[0]) == 6:
        #     maxLength = 128
        # else:
        #     print key
        try:
            maxLength = int(ip[1])
            if maxLength < prefixLength:
                continue # To skip the prefix's in which the maxLength is less that the prefix length.
        except IndexError:
            # In case the maxLength didn't exist.
            maxLength = prefixLength
        if AS in Trie_dict:
            if key in Trie_dict[AS]:
                Trie_dict[AS][key][3] = max(maxLength,Trie_dict[AS][key][3])
            else:
                Trie_dict[AS][key] = [Time, AS, prefix, maxLength]
        else:
            Trie_dict[AS] = ipReady(Time,AS, prefix, maxLength,key)

    file.close()
    # print "Number of ip's is:", rip
    return Trie_dict

def getDictTXT(filename):
    Trie_dict = {}
    file = open(filename, 'r')
    roa = 0
    rip = 0
    for line in file:
        roa += 1
        line = line[:-1].split(' ')
        Time = ''
        AS = line[1]
        IP = line[2:]
        for ip in IP:
            rip += 1
            ip = ip.split('-')
            prefix = ip[0]
            # print prefix
            key = prefix_to_key(prefix)
            # print key
            prefixLength = len(key.split('$')[1])
            try:
                maxLength = int(ip[1])
                if maxLength < prefixLength:
                    continue # To skip the prefix's in which the maxLength is less that the prefix length.
            except IndexError:
                # In case the maxLength didn't exist.
                maxLength = prefixLength
                # print maxLength
            if AS in Trie_dict:
                if key in Trie_dict[AS]:
                    Trie_dict[AS][key][3] = max(maxLength,Trie_dict[AS][key][3])
                else:
                    Trie_dict[AS][key] = [Time, AS, prefix, maxLength]
            else:
                Trie_dict[AS] = ipReady(Time,AS, prefix, maxLength,key)

    print "ROA's :", roa
    print "IP's :", rip
    file.close()
    return Trie_dict

def ipReady(Time,AS,prefix, maxLength,key):
    return {key: [Time, AS, prefix, maxLength]}

def mid_compress_list(ASList,mDict):
    def final_compress(Trie):
        def compress_Tries(node):
            ''' This function compresses the prefix's '''
            if node is None or not node.children:
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

            # Check if the node is an prefix (not just a connecting node) and that 2 children exist with prefix's and value's
            if node.value is not NULL and fchild.value is not NULL and schild is not None and schild.value is not NULL:
                # print 'HI!'
                # To check if the maxLength of the parent is higher or equal to the max(children's  maxLength)
                if node.value[3] >= maxML([fchild, schild]):
                    pass # No need to change the maxLength in this case.
                else:
                    # Only update the max length of the parent if it's less than the max of children
                    node.value[3] = minML([fchild, schild])
                # Only hide a child if the parent's max length is covering the child's max length
                # b_list = [node,fchild,schild]
                # print 'before:',b_list
                if node.value[3] >= fchild.value[3]:
                    key = prefix_to_key(fchild.value[2])
                    del Trie[key]
                    # del b_list[1]
                # Only hide a child if the parent's max length is covering the child's max length
                if node.value[3] >= schild.value[3]:
                    key = prefix_to_key(schild.value[2])
                    del Trie[key]
                    # del b_list[-1]
                # print 'after:',b_list
        def minML(childList):
            ''' This method should return the min of the children's maxLength'''
            numlist = list()
            for child in childList:
                numlist += [child.value[3]]  # Add the MaxLength to the list
            return min(numlist)
        def maxML(childList):
            ''' This method should return the max of the children's maxLength'''
            numlist = list()
            for child in childList:
                numlist += [child.value[3]]  # Add the MaxLength to the list
            return max(numlist)
        compress_Tries(Trie._root)
        return dict(Trie)


    for AS in ASList:
        t = Trie(**mDict[AS])
        mDict[AS] = final_compress(t)


def mid_compress(AS,mDict):
    def final_compress(Trie):
        def compress_Tries(node):
            ''' This function compresses the prefix's '''
            if node is None or not node.children:
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

            # Check if the node is an prefix (not just a connecting node) and that 2 children exist with prefix's and value's
            if node.value is not NULL and fchild.value is not NULL and schild is not None and schild.value is not NULL:
                # print 'HI!'
                # To check if the maxLength of the parent is higher or equal to the max(children's  maxLength)
                if node.value[3] >= maxML([fchild, schild]):
                    pass # No need to change the maxLength in this case.
                else:
                    # Only update the max length of the parent if it's less than the max of children
                    node.value[3] = minML([fchild, schild])
                # Only hide a child if the parent's max length is covering the child's max length
                # b_list = [node,fchild,schild]
                # print 'before:',b_list
                if node.value[3] >= fchild.value[3]:
                    key = prefix_to_key(fchild.value[2])
                    del Trie[key]
                    # del b_list[1]
                # Only hide a child if the parent's max length is covering the child's max length
                if node.value[3] >= schild.value[3]:
                    key = prefix_to_key(schild.value[2])
                    del Trie[key]
                    # del b_list[-1]
                # print 'after:',b_list
        def minML(childList):
            ''' This method should return the min of the children's maxLength'''
            numlist = list()
            for child in childList:
                numlist += [child.value[3]]  # Add the MaxLength to the list
            return min(numlist)
        def maxML(childList):
            ''' This method should return the max of the children's maxLength'''
            numlist = list()
            for child in childList:
                numlist += [child.value[3]]  # Add the MaxLength to the list
            return max(numlist)
        compress_Tries(Trie._root)
        return dict(Trie)

    t = Trie(**mDict[AS])
    mDict[AS] = final_compress(t)

def prefix_to_key(prefix):
    ''' A function given a prefix and AS generates a binary key to be used in a Trie.'''
    prefix = netaddr.IPNetwork(prefix)
    address = prefix.ip.bits().replace(".", "").replace(":","")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1

    # Building the key
    # No need for the first '$', the root is one at the begining.
    key = str(prefix.version) + '$'
    key +=  address
    return key

def print_dict(Dict):
    ''' Print all the data '''
    for AS in Dict.values():
        for prefix in AS.values():
            print str(prefix[0]) ,  str(prefix[1]) , str(prefix[2]) +'-'+ str(prefix[3])


IPfilenameCSV = "/home/osagga/Documents/compress-roas/Data_files/bgp_valid_announcements.txt"
# IPfilenameCSV = "/home/osagga/Documents/compress-roas/Data_files/bgp_announcements.txt"

# You switch between these two depending on the format of your input

# Trie_Dict = getDictTXT(IPfilenameTXT)
Trie_Dict = getDictCSV(IPfilenameCSV)

# This is just a counter of how many prefix's in all of the Tries.
before = sum([len(Trie_Dict[key]) for key in Trie_Dict.keys()])

def compress_multi():
    manager = Manager()
    pool = Pool(cpu_count())
    print "Running in parallel over", cpu_count(), "cores"
    suTrieDict = manager.dict(Trie_Dict)
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

    keylists = chunks(Trie_Dict.keys(),len(Trie_Dict.keys())/(cpu_count()))
    # This loop is just to check if the key's are actually divided.
    # for keylist in keylists:
        # print keylist
    [pool.apply_async(mid_compress_list, (keylist,suTrieDict)) for keylist in keylists]
    pool.close()
    pool.join()
    return suTrieDict

def compress_seq():
    [mid_compress(key,Trie_Dict) for key in Trie_Dict.keys()]

# print_dict(Trie_Dict)


begin = time.time()
compress_seq()
#Trie_Dict = compress_multi()
end = time.time()
print "total compression time:", end- begin, "seconds"

# This is another counter that does the same as 'before'.
after = sum([len(Trie_Dict[key]) for key in Trie_Dict.keys()])


diff = before - after
p = float(diff / float(before)) * 100.0

# print_dict(Trie_Dict)

print "Number of prefix's (ROA's):",len(Trie_Dict)
print "Number of prefix's before:",before
print "Number of prefix's after:",after
print p, '%'
