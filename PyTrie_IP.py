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

def ipReady(prefix, AS,maxLength = None):
    key = binTools.prefix_to_key(prefix)
    if maxLength is None :
        maxLength = len(key) - 2 #Because the '$' and v number {4,6}
    AS = int(AS)
    return {key: [maxLength, AS,prefix]}

IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/roa_list.txt"
t = Trie(getDict(IPfilename))

#t.combine_items()

# print t._find('$41000000000001000').children
# print t._find('$41000000000001000').children.get('0')
# print type(t._find('$41000000000001000').children.get('0'))
# print type(t._find('$41000000000001000').children.iter().next())

print t.dec_items()
