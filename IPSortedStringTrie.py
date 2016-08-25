#! /usr/bin/python
from pytrie import StringTrie as trie, NULL, Node as node


class nodeS(node):
    __slots__ = ('value', 'children', 'show')

    def __init__(self, value=NULL):
        self.value = value
        self.children = self.ChildrenFactory()
        self.show = True

    def __repr__(self):
        return str(self.value[0]) + ' ' + str(self.value[1]) + ' ' + str(self.value[2]) + '-' + str(self.value[3])


class Trie(trie):
    NodeFactory = nodeS

    def dec_items(self):
        '''Return a list or a string of this trie's nodes "Prefix,AS").
        '''
        for node in self.dec_iternodes():
            print node
        return

    def dec_iternodes(self):
        '''Return an iterator over this trie's nodes).

        '''
        parts = []
        append = parts.append

        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL and node.show:
                yield node
            for part, child in node.children.iteritems():
                append(part)
                for subresult in generator(child):
                    yield subresult
                del parts[-1]
        node = self._root
        return generator(node)

    def combine_items(self):
        rnode = self._root
        self.dfs_items(rnode)

    def dfs_items(self, node):
        if node is None or not node.children:
            return

        g = node.children.iteritems()

        lchild = node.children.get(str(g.next()[0]))
        try:
            rchild = node.children.get(str(g.next()[0]))
        except StopIteration:
            rchild = None

        self.dfs_items(lchild)
        self.dfs_items(rchild)
        if lchild is not None and node.value is not NULL and rchild is not None and lchild.value is not NULL and rchild.value is not NULL:
            if node.value[3] >= maxML([lchild, rchild]):
                pass
            else:
                node.value = [node.value[0], node.value[1], node.value[2], minML([lchild, rchild])]

            if node.value[3] >= lchild.value[3]:
                lchild.show = False
            if node.value[3] >= rchild.value[3]:
                rchild.show = False


def minML(childList):
    ''' This method should return back the min of the children maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[3]]  # Add the MaxLength to the list
    return min(numlist)

def maxML(childList):
    ''' This method should return back the min of the children maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[3]]  # Add the MaxLength to the list
    return max(numlist)
