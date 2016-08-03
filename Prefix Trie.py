# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 10:47:45 2016
@author: Omar Sagga
"""
import map_functions as binTools
import netaddr

NUM_CHILD = 2


class Node(object):
    ''' Trie Node class for the IP prefix Trie '''
    __slots__ = ['children', 'endsPath', 'prefix', 'AS', 'MaxLength']

    def __init__(self):
        self.children = [None] * NUM_CHILD
        self.endsPath = False

    def setAS(self, AS):
        self.AS = AS

    def getAS(self):
        return self.AS

    def setPrefix(self, Prefix):
        self.prefix = Prefix

    def getPrefix(self):
        return self.prefix

    def getBinRepr(self):
        return binTools.prefix_to_key(str_to_prefixObj(self.prefix))

    def setMaxLength(self, ML):
        self.MaxLength = ML

    def getMaxLength(self):
        return self.MaxLength

    def setChild(self, chNum, n):
        self.children[chNum] = n

    def getChild(self, chNum):
        return self.children[chNum]

    def setEndsPath(self, endsPath):
        self.endsPath = endsPath

    def getEndsPath(self):
        return self.endsPath

    def maxL_child(self):
        return [x.MaxLength for x in self.children]

    def __repr__(self):
        return "IP Prefix: " + self.prefix + '-' + str(self.MaxLength) + "  AS " + str(self.AS)


def str_to_prefixObj(str):
    return netaddr.IPNetwork(str)


class Trie(object):

    def __init__(self):
        self.root = Node()  # The Head of the tree
        self.PrefList = list()  # The prefix list

    def getPrefixList(self):
        return self.PrefList

    def add(self, prefix, AS):
        binIP = binTools.prefix_to_key(str_to_prefixObj(prefix))
        self.addHelper(self.root, binIP, prefix, AS, len(binIP))

    def addHelper(self, n, bit, prefix, AS, ML):
        if bit == '':
            # To hold the prefix, AS# and Max length info in the last Node.
            n.setAS(AS)
            n.setMaxLength(ML)
            n.setPrefix(prefix)

            n.setEndsPath(True)

            # To merge and combin IP prefix's (The main this of this code)
            for child in n.children:
                if child == None or child.getAS() != n.getAS():
                    return

            # If the conditions succead
            n.setMaxLength(min(n.maxL_child()))

            # To hide the IP prefix's of the child that got merged with parents
            n.children[0].setEndsPath(False)
            n.children[1].setEndsPath(False)

            return

        f_bit = int(bit[0])

        child = n.getChild(f_bit)

        if (child == None):
            newNode = Node()
            n.setChild(f_bit, newNode)
            self.addHelper(newNode, bit[1:], prefix, AS, ML)
        else:
            self.addHelper(child, bit[1:], prefix, AS, ML)

    def printKey(self):
        self.printKeysHelper(self.root)

    def printKeysHelper(self, n):
        if n == None:
            return

        if (n.getEndsPath()):
            print n  # Print's the IP prefix
            self.PrefList.append(n)  # To append to the Prefix List

        for char in range(len(n.children)):
            if n.children[char] == None:
                continue
            self.printKeysHelper(n.children[char])


print "This is a test of Class Trie!"
print "[1] Creating a Trie Node and insearting 4 Prefix's :"

t = Trie()
# Adding the bottom 4 Prefix's
t.add('128.8.0/18', 1)
# t.add('128.8.64/18',1)  # Adding this will make '128.8/16' combine and
# extend to 18.
t.add('128.8.192/18', 1)
t.add('128.8.128/18', 1)

# Adding the /17 Prefix's
t.add('128.8.128/17', 1)
t.add('128.8.0/17', 1)

# Adding the main /16 Prefix
t.add('128.8/16', 1)

# Adding a random IP prefix for testing
t.add('10.233.0.3/32', 2)

t.printKey()
print(t.getPrefixList())  # To print them as a list
