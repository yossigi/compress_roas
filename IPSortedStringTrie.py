from pytrie import StringTrie as trie, NULL, Node as node


class nodeS(node):
    __slots__ = ('value', 'children', 'show')

    def __init__(self, value=NULL):
        self.value = value
        self.children = self.ChildrenFactory()
        self.show = True


class Trie(trie):
    NodeFactory = nodeS

    def dec_items(self, prefix=None):
        '''Return a list or a string of this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, return only the items associated with keys
            prefixed by ``prefix``.
        '''
        #s = str()
        l = list()
        for item in self.dec_iteritems(prefix):
            l += [item]
            #s += str(item) + '\n'

        return l
        #return s

    def dec_iteritems(self, prefix=None):
        '''Return an iterator over this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, yield only the items associated with keys
            prefixed by ``prefix``.
        '''
        parts = []
        append = parts.append

        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL and node.show:
                #print node.value
                key = "Prefix: " + \
                    str(node.value[2])
                key += '-' + str(node.value[0])
                key += "  AS " + str(node.value[1])
                yield key  # This is the line I changed
            for part, child in node.children.iteritems():
                append(part)
                for subresult in generator(child):
                    yield subresult
                del parts[-1]
        node = self._root
        if prefix is not None:
            for part in prefix:
                append(part)
                node = node.children.get(part)
                if node is None:
                    node = self.NodeFactory()
                    break
        return generator(node)

    def combine_items(self):
        rnode = self._root
        self.dfs_items(rnode)

    def dfs_items(self, node):
        # print 'This is my node : ' ,node
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
        if lchild is not None and node.value is not NULL and rchild is not None and lchild.value is not NULL and rchild.value is not NULL and lchild.value[1] == node.value[1] and rchild.value[1] == node.value[1]:
            # Update the maxLength of the parent.
            node.value = [minML([lchild, rchild]), node.value[1],node.value[2]]
            lchild.show = False  # Hide this node in the tree
            rchild.show = False  # Hide this node in the tree

            # In case the parent would hide a child whose children are not
            # included in the parent's maxLength
            if node.value[0] < lchild.value[0]:
                lchild.show = True
            if node.value[0] < rchild.value[0]:
                rchild.show = True


def minML(childList):
    ''' This method should return back the min of the children maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[0]]  # Add the MaxLength to the list
    return min(numlist)
