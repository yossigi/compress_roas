# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016

@author: Omar Sagga
"""
import map_functions as binTools
from pygtrie import CharTrie as trie

t = trie()
dic = dict()
file = open('ip_list.txt','r')

def ipReady(prefix,AS):
    key = binTools.prefix_to_key(prefix)
    maxLength = len(key)
    AS = AS
    return {key:[maxLength,AS]}
    
def addTo(dict_ip):
    return trie(dict_ip)
    
for line in file:
    ip = line[:-1].split(',')
    dic.update(ipReady(ip[0].strip(),ip[1].strip()))


file.close()
t = addTo(dic)

#print binTools.prefix_to_key('128.8.128/17') 
#print binTools.prefix_to_key('128.8.128/18')
#print binTools.prefix_to_key('128.8/16')
 
print [x for x in t.items('1000000000001000') if int(x[1][0]) == len('1000000000001000') + 1]
#print t.has_subtrie('10000000000010001')    #128.8.128/17
#print t.has_subtrie('100000000000100010')   #128.8.128/18
print t.has_subtrie('1000000000001000')   #128.8/16
#print t.__path_from_key('100000000000100010')
#print t.has_node('10000000000010001')    #128.8.128/17
#print t.has_node('100000000000100010')   #128.8.128/18
#print t.has_node('1000000000001000')   #128.8/16
print t.items('10000000000010001'),'\n'    #128.8.128/17
#print t.prefixes('100000000000100010'),'\n'  #128.8.128/18
print t.items('1000000000001000'),'\n' #128.8/16
print type(t.longest_prefix('1000000000001000')),'\n' #128.8/16

print '#\n',t.keys()

