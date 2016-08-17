# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016
@author: Omar Sagga
"""

import map_functions as binTools
from IPSortedStringTrie import Trie


def getDict(filename):
    IPdict = dict()
    file = open(filename, 'r')
    g = file.__iter__()
    g.next()
    for line in file:
        line = line[:-1].split(',')
        #print 'This is the line :', line
        AS = line[0]
        IP = line[1]
        ip = IP.split('-')
        prefix = ip[0]
        try:
            maxLength = ip[1]
        except IndexError:
            maxLength = None
        #print prefix,AS,maxLength
        IPdict.update(ipReady(prefix, AS, maxLength))

    file.close()
    return IPdict


def ipReady(prefix, AS, maxLength=None):
    key = binTools.prefix_to_key(prefix)
    if maxLength is None:
        maxLength = len(key) - 2  # Because the '$' and v number {4,6}
    AS = int(AS)
    return {key: [maxLength, AS, prefix]}

IPfilename = "C:\Users\osagg\Documents\ROA_PyTrie\/all_prefixes_list.csv"
#IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/valid_prefixes_list.csv"
# IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/valid_prefixes_list.csv"
t = Trie(getDict(IPfilename))

before = t.dec_items()
t.combine_items()
after = t.dec_items()
diff= len(before) - len(after)
p = float(diff/float(len(before))) * 100.0
print len(before)
print len(after)
print 'Diff:', len(before) - len(after)
print p,'%'

#In use :)
