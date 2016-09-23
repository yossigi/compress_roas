# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016
@author: Omar Sagga
"""

import resource
import map_functions as binTools
from IPSortedStringTrie import Trie, NULL
from multiprocessing import Process, Manager, Pool,cpu_count

def getDictCSV(filename):
    IPdict = dict()
    Trie_dict = {}
    rip = 0
    file = open(filename, 'r')
    for line in file:
        rip += 1
        line = line[:-1].split(',')
        AS = line[1]
        IP = line[0]
        Time = '13:37'
        ip = IP.split('-')
        prefix = ip[0]
        key = binTools.prefix_to_key(prefix)
        prefixLength = len(key.split('$')[1])
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

    for AS in Trie_dict:
        Trie_dict[AS] = Trie(**Trie_dict[AS])
    file.close()
    print "Number of ip's is:", rip
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
            key = binTools.prefix_to_key(prefix)
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

    for AS in Trie_dict:
        Trie_dict[AS] = Trie(**Trie_dict[AS])
    print "ROA's :", roa
    print "IP's :", rip
    file.close()
    return Trie_dict

def ipReady(Time,AS,prefix, maxLength,key):
    return {key: [Time, AS, prefix, maxLength]}

def mid_compress(AS,mDict):
    ''' This function starts the DFS starting from the root of the Trie.'''
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
                if node.value[3] >= fchild.value[3]:
                    key = binTools.prefix_to_key(fchild.value[2])
                    del Trie[key]
                # Only hide a child if the parent's max length is covering the child's max length
                if node.value[3] >= schild.value[3]:
                    key = binTools.prefix_to_key(schild.value[2])
                    del Trie[key]
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
        return Trie
    mDict[AS] = final_compress(mDict[AS])

def print_dict(Dict):
    for AS in Dict.values():
        for prefix in AS.dec_iternodes():
            print prefix


# IPfilenameCSV = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/bgp_valid_announcements\/bgp_valid_announcements.csv"
# IPfilenameTXT = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/roa_list_new.txt"
# IPfilenameTXT = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/ip_list.txt"
IPfilenameTXT = "/home/osagga/Documents/compress-roas/Data files/roa_list.txt"
# IPfilenameCSV = "/home/osagga/Documents/compress-roas/Data files/bgp_announcements.txt"
# IPfilenameTXT = "/home/osagga/Documents/compress-roas/Data files/ip_list.txt"
# IPfilenameCSV = "/home/osagga/Documents/compress-roas/Data files/all_prefixes_list.csv"

Trie_Dict = getDictTXT(IPfilenameTXT)
# Trie_Dict = getDictCSV(IPfilenameCSV)

def compress():
    manager = Manager()
    pool = Pool(8)
    suTrieDict = manager.dict(Trie_Dict)
    [pool.apply_async(mid_compress, (key,suTrieDict)) for key in suTrieDict.keys()]
    # [mid_compress(key,suTrieDict) for key in suTrieDict.keys()]
    pool.close()
    pool.join()
    return suTrieDict


before = sum([len(Trie_Dict[AS].dec_items()) for AS in Trie_Dict.keys()])
# print_dict(Trie_Dict)
[mid_compress(AS,Trie_Dict) for AS in Trie_Dict.keys()]

# Trie_Dict = compress()

after = sum([len(Trie_Dict[AS].dec_items()) for AS in Trie_Dict.keys()])


diff = before - after
p = float(diff / float(before)) * 100.0


# print before
print_dict(Trie_Dict)
# # print len(Trie_Dict)
# print after
# print p, '%'
