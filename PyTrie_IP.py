# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016

@author: Omar Sagga
"""


from IPSortedStringTrie import Trie
from IP_DictMaker import getDict


IPfilename = "C:\Users\osagg\Documents\ROA_PyTrie\ip_list.txt"
dict = getDict(IPfilename)
t = Trie(dict)


def getDefaultChild(key):
    ''' This will auto-generate the supposed children of a prefix.'''
    l = list()
    l += [key + '0']
    l += [key + '1']
    return l


def minML(childList):
    ''' This method should return back the min of the children maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[0]]  # Add the MaxLength to the list
    return min(numlist)


def TuneKey(dkey):
    ''' This method should do the magic (combine the parent with child if possible) '''

    dchildlist = getDefaultChild(dkey)  # The auto-generated children's
    rchildlist = list()  # The real children Node's from the Trie

    for child in dchildlist:
        # Check if the supposed Child is in the SubTrie under the parent.
        ckey = t._find(child)  # The node of each child if there exists such.
        nkey = t._find(dkey)  # The node of the inserted key.

        # To check if the child exist's and AS's match.
        if ckey is None or ckey.value[1] != nkey.value[1]:
            return
        # ckey.
        rchildlist += [ckey]
    if len(rchildlist) == len(dchildlist):
        for child in rchildlist:
            child.show = False
        nkey.show = True
        # I'm just updating the maxLength of the Prefix.
        nkey.value = [minML(rchildlist), rchildlist[0].value[1]]


def Tuneall():
    for key in t:
        TuneKey(key)


Tuneall()
print t.dec_items()
