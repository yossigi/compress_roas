#! /usr/bin/python
#
# $Id: scan_roas 5856 2014-05-31 18:32:19Z sra $
"""
Created on Wed Aug 03 12:14:35 2016
@author: Omar Sagga
"""
import os
import argparse
from IPSortedStringTrie import Trie
import map_functions as binTools
import subprocess


def check_dir(d): # Copyright (C) 2014 Dragon Research Labs
  if not os.path.isdir(d):
    raise argparse.ArgumentTypeError("%r is not a directory" % d)
  return d

parser = argparse.ArgumentParser(description = __doc__) # Copyright (C) 2014 Dragon Research Labs
parser.add_argument("rcynic_dir", nargs = "+", type = check_dir, # Copyright (C) 2014 Dragon Research Labs
                     help = "rcynic authenticated output directory")

args = parser.parse_args() # Copyright (C) 2014 Dragon Research Labs

terminal = subprocess.Popen(['scan_roas' , args.rcynic_dir[0] ], stdout=subprocess.PIPE)
output = terminal.communicate()[0]


def getDict(output):
    IPdict = dict()
    output = output[:-1].split('\n')
    for line in output:
        line = line.split(' ')
        Time = line[0]
        AS = int(line[1])
        IP = line[2:]
        for ip in IP:
            ip = ip.split('-')
            prefix = ip[0]
            key = binTools.prefix_to_key(prefix, AS)
            try:
                maxLength = int(ip[1])
            except IndexError:
                maxLength = len(key) - 3 - len(bin(AS)) # Because the '$' and v number {4,6} and '?' and AS
            if key in IPdict:
                IPdict[key] = [Time,AS,prefix,max(maxLength,IPdict[key][3])]
            else:
                IPdict.update(ipReady(Time,AS, prefix, maxLength,key))

    return IPdict


def ipReady(Time,AS,prefix, maxLength,key):
    return {key: [Time, AS, prefix, maxLength]}

t = Trie(getDict(output))

# t.combine_items()
t.dec_items()
