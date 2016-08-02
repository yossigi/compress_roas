# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 10:47:45 2016
@author: Moe Sagga
"""

NUM_CHILD = 2
OCTET_SIZE = 8


class Node(object):
    ''' Trie Node class for the IP prefix Trie '''
    __slots__ = ['children', 'endsPath', 'dec_IP', 'AS', 'MaxLength']

    def __init__(self):
        self.children = [None] * NUM_CHILD
        self.endsPath = False

    def setAS(self, AS):
        self.AS = AS

    def getAS(self):
        return self.AS

    def setPrefix(self, Prefix):
        self.dec_IP = Prefix

    def getPrefix(self):
        return self.dec_IP

    def getBinRepr(self):
        return dec_to_bin(self.getPrefix(self.dec_IP))[:int(self.getMaxLength())]

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
        return "IP Prefix: " + self.dec_IP + "/" + self.MaxLength + "  AS " + str(self.AS)


def dec_to_bin(IP):
    ''' Converts from the decimal represination of the IP prefix
            to a binary one to use for saving in the Trie.
    '''
    bin_repr = ''
    IP = IP.split('.')
    for octet in IP:
        if octet == '':
            continue
        temp = str(bin(int(octet))[2:])  # To remove the '0b' at the beginning
        if len(temp) < OCTET_SIZE:
            temp = '0' * (OCTET_SIZE - len(temp)) + temp #To fill the rest of the string with 0's (to make sure it'll be 8 bits)
        bin_repr += temp

    return bin_repr


def bin_to_dec(IP):
    ''' The opposite of dec_to_bin() '''
    dec_repr = ''
    while(len(IP) > OCTET_SIZE): #So that you stop and don't add a '.' at the end.
        dec_repr += str(int(IP[:OCTET_SIZE], 2)) + '.'
        IP = IP[OCTET_SIZE:]
    dec_repr += str(int(IP[:OCTET_SIZE], 2))

    return dec_repr


class Trie(object):

    def __init__(self):
        self.root = Node() #The Head of the tree

    def add(self, prefix, AS):

        prefix = prefix.split('/')  # Split so that you can get rid of the end of the prefix "/32"
        # This will cut the binary repr of the IP prefix to the max length
        binIP = dec_to_bin(prefix[0])[:int(prefix[1])]

        self.addHelper(self.root, binIP, prefix[0], AS, prefix[1])

    def addHelper(self, n, bit, prefix, AS, ML):
        if bit == '':
            # To hold the prefix, AS# and Max length info in the last Node.
            n.setAS(AS)
            n.setMaxLength(ML)
            n.setPrefix(prefix)
            #(debugging) To know what has been added
            # print n

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

        for char in range(len(n.children)):
            if n.children[char] == None:
                continue
            self.printKeysHelper(n.children[char])

def main():
    print "This is a test of Class Trie!"
    print "[1] Creating a Trie Node and insearting 4 Prefix's :"

    t = Trie()
    # Adding the bottom 4 Prefix's
    t.add('128.8.0/18', 1)
    # t.add('128.8.64/18',1)  # Adding this will make '128.8/16' combine and extend to 18.
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


main()
