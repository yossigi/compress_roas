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
    # g = file.__iter__()
    # g.next()
    for line in file:
        # i += 1
        line = line[:-1].split(',')
        AS = int(line[1])
        IP = line[0]
        Time = '13:37'
        ip = IP.split('-')
        prefix = ip[0]
        key = binTools.prefix_to_key(prefix,AS)
        try:
            # maxLength = int(ip[1])
            maxLength = 32
        except IndexError:
            maxLength = len(key) - 3 - len(str(bin(AS))[2:]) # Because the '$' and v number {4,6}
        # print key
        if key in IPdict:
            IPdict[key] = [Time,AS,prefix,max(maxLength,IPdict[key][3])]
        else:
            IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    file.close()
    # print 'Number of lines is:', i
    return IPdict

def getDictTXT(filename):
    IPdict = dict()
    file = open(filename, 'r')
    i = 0
    full_dub = list()
    semi_dub = list()
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
            try:
                maxLength = int(ip[1])
            except IndexError:
                maxLength = len(key) - 3 - len(str(bin(AS))[2:]) # Because the '$' and v number {4,6} and '?' and AS
            # print key
            if key in IPdict:
                if maxLength == IPdict[key][3]:
                    full_dub += ["prefix: " + str(prefix) + " AS: " + str(AS) + " maxLength: " + str(maxLength)]
                else:
                    semi_dub += ["@prefix: " + str(prefix) + " AS: " + str(AS) + " maxLength: " + str(maxLength)]
                IPdict[key] = [Time,AS,prefix,max(maxLength,IPdict[key][3])]
            else:
                IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    print 'Number of lines is:', i
    for ip in full_dub:
        print ip
    for ip in semi_dub:
        print ip
    # print full_dub
    # print semi_dub
    print len(full_dub)
    print len(semi_dub)
    file.close()
    return IPdict

def ipReady(Time,AS,prefix, maxLength,key):
    return {key: [Time, AS, prefix, maxLength]}


# IPfilenameCSV = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/ipv4_bgp_announcements.csv"
# IPfilenameCSV = "C:\Users\OSAGGA\Documents\ROA_PyTrie\/test.csv"
IPfilenameCSV = "C:\Users\osagg\Documents\ROA_PyTrie\Data files\ipv4_bgp_announcements.csv"
# IPfilenameTXT = "C:\Users\OSAGGA\Documents\ROA_PyTrie\Output files\/roa_list_new.txt"
# IPfilenameTXT = "C:\Users\osagg\Documents\ROA_PyTrie\Data files\/roa_list_new.txt"


t = Trie(getDictCSV(IPfilenameCSV))
# t = Trie(getDictTXT(IPfilenameTXT))

before = t.dec_items()

# print 'All-Before:',before + '\n'
# Here I do the minimizing of the ROA's
t.combine_items()

after = t.dec_items()

diff = len(before) - len(after)
p = float(diff / float(len(before))) * 100.0


# print 'All-After:',after

print len(before)
print len(after)
print p, '%'
