# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016

@author: Omar Sagga
"""
import map_functions as binTools
from pytrie import SortedStringTrie as trie

file = open('ip_list.txt','r')

t = trie()

def ipReady(prefix,AS):
    key = binTools.prefix_to_key(prefix)
    maxLength = len(key)
    AS = int(AS)
    return {key:[maxLength,AS]}

for line in file:
    ip = line[:-1].split(',')
    t.update(ipReady(ip[0].strip(),ip[1].strip())) #Update the Trie.
file.close()



def getDefaultChild(key):   #This will auto-generate the supposed children of a prefix.
    l = list()
    l += [key + '0']
    l += [key + '1']
    return l
    

def minML(keylist):         #This method should return back the min of the children maxLength
    numlist = list()
    for key in keylist:
        numlist += [key.value[0]] #Add the MaxLength to the list
    return min(numlist)


def TuneKey(dkey):   #This method should do the magic (combine the parent with child if possible)
    
    dchildlist = getDefaultChild(dkey)  #The auto-generated children's
    rchildlist = list()                 #The real children Node's from the Trie
    
    for child in dchildlist:
        nkey = t._find(dkey)            #Check if the supposed Child is in the SubTrie under the parent.
        ckey = t._find(child)
        
        if ckey is None:                 #To check if the child exist's
            return
        if ckey.value[1] != nkey.value[1]:     #To check if the AS's match
            return
        
        rchildlist += [ckey]
    
    t.update({dkey:[minML(rchildlist),rchildlist[0].value[1]]})
    

def Tuneall():
    for key in t:
        TuneKey(key)

Tuneall()
Tuneall()
print t.values()


