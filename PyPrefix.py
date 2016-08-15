# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016
@author: Omar Sagga
"""

import map_functions as binTools
from IPSortedStringTrie import Trie
import subprocess


test = subprocess.Popen('scan_roas /home/bingo/Documents/ROA_Project/authenticated'.split(), stdout=subprocess.PIPE)
output = test.communicate()[0]


def getDict(filename):
    IPdict = dict()
    file = open(filename, 'r')
    for line in file:
        line = line[:-1].split(' ')
        AS = line[1]
        IP = line[2:]
        for ip in IP:
            ip = ip.split('-')
            prefix = ip[0]
            try:
                maxLength = ip[1]
            except IndexError:
                maxLength = None
            IPdict.update(ipReady(prefix, AS, maxLength))
    file.close()
    return IPdict


def ipReady(prefix, AS, maxLength=None):
    key = binTools.prefix_to_key(prefix)
    if maxLength is None:
        maxLength = len(key) - 2  # Because the '$' and v number {4,6}
    AS = int(AS)
    return {key: [maxLength, AS, prefix]}

#IPfilename = "/home/bingo/Documents/ROA_Project/PyPrefix/ip_list.txt"
#IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/ip_list.txt"
# IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/valid_prefixes_list.csv"
#IPfilename = "/home/bingo/Documents/ROA_Project/PyPrefix/\valid_prefixes_list.csv"
t = Trie(getDict(output))


t.combine_items()
#t.dec_items()
#diff= len(before) - len(after)
#p = float(diff/float(len(before))) * 100.0
#print len(before)
#print len(after)
#print after
#print diff
#print p,'%'
