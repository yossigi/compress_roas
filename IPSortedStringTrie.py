from pytrie import SortedStringTrie as trie, NULL, Node as node



class nodeS(node):
    ''' a Sub-class of the original 'node', I just changed the way the node is being represented in.'''

    def __repr__(self):
        ''' It's this format: [Time] [ASN] [IP_Prefix (with prefixLength)] [maxLength] '''
        return str(self.value[0]) + ' ' +  str(self.value[1]) + ' ' + str(self.value[2]) + '-' + str(self.value[3])

class Trie(trie):
    ''' use the modfified class I created.'''
    NodeFactory = nodeS

    def dec_items(self):
        '''print all the nodes you get from the generator "dec_iternodes()". '''

        for node in self.dec_iternodes():
            print node

    def dec_iternodes(self):
        '''Return an iterator over this trie's nodes. '''
        parts = []
        append = parts.append

        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL:
                # Return the node itself back.
                yield node
            for part, child in node.children.iteritems():
                append(part)
                for subresult in generator(child):
                    yield subresult
                del parts[-1]
        node = self._root
        return generator(node)
