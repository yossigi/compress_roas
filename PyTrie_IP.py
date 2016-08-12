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
    for line in file:
        line = line[:-1].split(' ')
        AS = line[1]
        IP = line[2:]
        for ip in IP :
            ip = ip.split('-')
            prefix = ip[0]
            try :
                maxLength = ip[1]
            except IndexError:
                maxLength = None
            IPdict.update(ipReady(prefix, AS,maxLength))
    file.close()
    return IPdict

def ipReady(prefix, AS, maxLength = None):
    key = binTools.prefix_to_key(prefix)
    if maxLength is None :
        maxLength = len(key) - 2 #Because the '$' and v number {4,6}
    AS = int(AS)
    return {key: [maxLength, AS, prefix]}

IPfilename = "C:\Users\osagg\Documents\ROA_PyTrie\/ip_list.txt"
t = Trie(getDict(IPfilename))

print len(t.dec_items())
t.combine_items()
print len(t.dec_items())
