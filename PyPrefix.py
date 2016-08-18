# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016
@author: Omar Sagga
"""

import map_functions as binTools
from IPSortedStringTrie import Trie


def getDictCSV(filename):
    IPdict = dict()
    i = 0
    file = open(filename, 'r')
    g = file.__iter__()
    g.next()
    for line in file:
        i += 1
        line = line[:-1].split(',')
        AS = int(line[0])
        IP = line[1]
        Time = '13:37'
        ip = IP.split('-')
        prefix = ip[0]
        key = binTools.prefix_to_key(prefix,AS)
        try:
            maxLength = int(ip[1])
        except IndexError:
            maxLength = len(key) - 2 - len(bin(AS)) # Because the '$' and v number {4,6}
        IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    file.close()
    print 'Number of lines is:', i
    return IPdict

def getDictTXT(filename):
    IPdict = dict()
    file = open(filename, 'r')
    i = 0
    dub = list()
    for line in file:
        line = line.split(' ')
        Time = line[0]
        AS = int(line[1])
        IP = line[2:]
        for ip in IP:
            i += 1
            ip = ip.split('-')
            prefix = ip[0]
            key = binTools.prefix_to_key(prefix,AS)
            try:
                maxLength = int(ip[1])
            except IndexError:
                maxLength = len(key) - 2 - len(bin(AS)) # Because the '$' and v number {4,6}
            if key in IPdict:
                dub += [prefix]
            else:
                IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    print 'Number of lines is:', i
    print len(dub)
    file.close()
    return IPdict

def ipReady(Time,AS,prefix, maxLength,key):
    return {key: [Time, AS, prefix, maxLength]}


#IPfilenameCSV = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/valid_prefixes_list.csv"
IPfilenameCSV = "C:\Users\osagg\Documents\ROA_PyTrie\/valid_prefixes_list.csv"
#IPfilenameTXT = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/roa_list.txt"
IPfilenameTXT = "C:\Users\osagg\Documents\ROA_PyTrie\/roa_list.txt"


t = Trie(getDictCSV(IPfilenameCSV))
# t = Trie(getDictTXT(IPfilenameTXT))

before = t.dec_items()

# Here I do the minimizing of the ROA's
t.combine_items()

after = t.dec_items()
diff = len(before) - len(after)
p = float(diff / float(len(before))) * 100.0
print len(before)
print len(after)
print p, '%'
# print after
