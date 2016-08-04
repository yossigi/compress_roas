# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016

@author: Omar Sagga
"""

from IPSortedStringTrie import Trie
from IP_DictMaker import getDict


IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie/ip_list.txt"
t = Trie()
t.update(getDict(IPfilename))


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
        nkey = t._find(dkey)
        ckey = t._find(child)

        if ckey is None:  # To check if the child exist's
            return
        if ckey.value[1] != nkey.value[1]:  # To check if the AS's match
            return

        rchildlist += [ckey]

    t.update({dkey: [minML(rchildlist), rchildlist[0].value[1]]}) #I'm just updating the maxLength of the Prefix.


def Tuneall():
    for key in t:
        TuneKey(key)

# It needs to be twice for now because the way the combining goes is not
# based on the sorting.
Tuneall()
Tuneall()
print t.f_items()  # It's diffrent from the normal t.items() because this will show the keys as a IPv* format (and also in a string instead of a list)
