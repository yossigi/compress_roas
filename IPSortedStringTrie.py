import map_functions as binTools
from pytrie import SortedStringTrie as trie, NULL
#from pytrie import NULL


def iteritems(d):
    return d.iteritems()


class Trie(trie):

    def f_items(self, prefix=None):
        '''Return a list of this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, return only the items associated with keys
            prefixed by ``prefix``.
        '''
        s = str()
        #l = list()
        for item in self.f_iteritems(prefix):
            #l += [item]
            s += str(item) + '\n'

        # return l
        return s

    def f_iteritems(self, prefix=None):
        '''Return an iterator over this trie's items (``(key,value)`` tuples).

        :param prefix: If not None, yield only the items associated with keys
            prefixed by ``prefix``.
        '''
        parts = []
        append = parts.append

        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL:
                key = "Prefix: " + str(binTools.key_to_prefix(key_factory(parts))) + \
                    '-' + str(node.value[0]) + "  AS " + str(node.value[1])
                yield (key, node.value)  # This is the line I changed
            for part, child in iteritems(node.children):
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
