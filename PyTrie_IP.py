# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:14:35 2016

@author: Omar Sagga
"""

from IP_DictMaker import getDict
IPfilename = "C:\Users\OSAGGA\Documents\ROA_PyTrie\ip_list.txt"
t = getDict(IPfilename)
print t.dec_items()
