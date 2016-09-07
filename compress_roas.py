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
    for line in file:
        i += 1
        line = line[:-1].split(',')
        AS = int(line[1])
        IP = line[0]
        Time = '13:37'
        ip = IP.split('-')
        prefix = ip[0]
        key = binTools.prefix_to_key(prefix,AS)
        prefixLength = len(key.split('$')[3])
        try:
            maxLength = int(ip[1])
            if maxLength < prefixLength:
                continue # To skip the prefix's in which the maxLength is less that the prefix length.
        except IndexError:
            # In case the maxLength didn't exist.
            maxLength = prefixLength
        if key in IPdict:
            IPdict[key][3] = max(maxLength,IPdict[key][3])
        else:
            IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    file.close()
    print 'Number of lines is:', i
    return IPdict

def getDictTXT(filename):
    IPdict = dict()
    file = open(filename, 'r')
    i = 0
    for line in file:
        line = line[:-1].split(' ')
        Time = ''
        AS = int(line[1])
        IP = line[2:]
        for ip in IP:
            i += 1
            ip = ip.split('-')
            prefix = ip[0]
            key = binTools.prefix_to_key(prefix,AS)
            # print key
            prefixLength = len(key.split('$')[3])
            # print key
            try:
                maxLength = int(ip[1])
                if maxLength < prefixLength:
                    continue # To skip the prefix's in which the maxLength is less that the prefix length.
            except IndexError:
                # In case the maxLength didn't exist.
                maxLength = prefixLength
            if key in IPdict:
                IPdict[key][3] = max(maxLength,IPdict[key][3])
            else:
                IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    # print 'Number of lines is:', i
    file.close()
    return IPdict

def ipReady(Time,AS,prefix, maxLength,key):
    return {key: [Time, AS, prefix, maxLength]}



# IPfilenameCSV = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/bgp_announcements\/bgp_announcements.csv"
# IPfilenameCSV = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/bgp_valid_announcements\/bgp_valid_announcements.csv"
IPfilenameTXT = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/roa_list_new.txt"
# IPfilenameTXT = "C:\Users\OSAGGA\Documents\compress_roas\Data files\/ip_list.txt"
# IPfilenameTXT = "C:\Users\osagg\Documents\ROA_PyTrie\Data files\/roa_list_new.txt"


# t = Trie(**getDictCSV(IPfilenameCSV))
t = Trie(**getDictTXT(IPfilenameTXT))

before = t.dec_items()

# print 'All-Before:',before

# print t.keys('$08699$')

# Here I do the minimizing of the ROA's
t.combine_items()

after = t.dec_items()

diff = len(before) - len(after)
p = float(diff / float(len(before))) * 100.0


# print 'All-After:',after

print len(before)
print len(after)
print p, '%'
