from pytrie import SortedStringTrie as trie, NULL, Node as node


class nodeS(node):
    __slots__ = ('value', 'children', 'show')

    def __init__(self, value=NULL):
        self.value = value
        self.children = self.ChildrenFactory()
        self.show = True
    def __repr__(self):
        return str(self.value[0]) + ' ' +  str(self.value[1]) + ' ' + str(self.value[2]) + '-' + str(self.value[3])

class Trie(trie):
    NodeFactory = nodeS

    def dec_items(self):
        '''Return a list or a string of this trie's nodes "Prefix,AS").

        '''
        for node in self.dec_iternodes():
            print node

    def dec_iternodes(self):
        '''Return an iterator over this trie's nodes "Prefix,AS").

        '''
        parts = []
        append = parts.append

        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL and node.show:
                yield node # I outputted the whole node so that I can get all the info from it.
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
            # When you reach a leaf node, just stop.
            return

        g = node.children.iteritems()

        # To get pointers on the children nodes.
        fchild = node.children.get(str(g.next()[0]))
        try:
            schild = node.children.get(str(g.next()[0]))
        # in case a second child doesn't exist.
        except StopIteration:
            schild = None

        # The recursive call to reach the end of the Trie.
        self.dfs_items(fchild)
        self.dfs_items(schild)

        # Check if the node is an prefix (not just a connecting node) and that 2 children exist with prefix's and value's
        if node.value is not NULL and fchild.value is not NULL and schild is not None and schild.value is not NULL:

            # To check if the maxLength of the parent is higher or equal to the max(children's  maxLength)
            if node.value[3] >= maxML([fchild, schild]):
                pass
            else:
                # Only update the max length of the parent if it's less than the max of children
                node.value = [node.value[0], node.value[1], node.value[2], minML([fchild, schild])]
            # Only hide a child if the parent's max length is covering the child's max length
            if node.value[3] >= fchild.value[3]:
                fchild.show = False
            # Only hide a child if the parent's max length is covering the child's max length
            if node.value[3] >= schild.value[3]:
                schild.show = False


def minML(childList):
    ''' This method should return back the min of the children's maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[3]]  # Add the MaxLength to the list
    return min(numlist)

def maxML(childList):
    ''' This method should return back the max of the children's maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[3]]  # Add the MaxLength to the list
    return max(numlist)
