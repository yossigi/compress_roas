# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016

@author: Omar Sagga
"""
# In order for the IP prefix's to be correctly combined, the prefix's need to be ordered that it goes from the smallest
# sub-prefix to the largest.


import map_functions as binTools
from IPSortedStringTrie import Trie


def getDict(filename):
    IPdict = Trie()
    file = open(filename, 'r')
    for line in file:
        line = line[:-1].split(',')
        # Update the Dict.
        ip = line[0].strip('"')
        AS = line[1].strip(' ')
        IPdict.update(ipReady(ip, AS))
    file.close()
    return IPdict


def ipReady(prefix, AS):
    key = binTools.prefix_to_key(prefix)
    maxLength = len(key) - 1
    AS = int(AS)
    return {key: [maxLength, AS]}

IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\ip_list.txt"
t = getDict(IPfilename)
print t.dec_items()
