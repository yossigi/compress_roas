import map_functions as binTools
from pytrie import SortedStringTrie as trie, NULL,Node as node

class NodeS(node):
    __slots__ = ('value', 'children','show')
    def __init__(self, value=NULL):
        self.value = value
        self.children = self.ChildrenFactory()
        self.show = True

class Trie(trie):
    NodeFactory = NodeS
    def dec_items(self, prefix=None):
        '''Return a list or a string of this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, return only the items associated with keys
            prefixed by ``prefix``.
        '''
        s = str()
        #l = list()
        for item in self.dec_iteritems(prefix):
            #l += [item]
            s += str(item) + '\n'

        # return l
        return s

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
                key = "Prefix: " + str(binTools.key_to_prefix(key_factory(parts))) + \
                    '-' + str(node.value[0]) + "  AS " + str(node.value[1])
                yield key # This is the line I changed
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
