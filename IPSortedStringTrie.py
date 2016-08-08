import map_functions as binTools
from pytrie import SortedStringTrie as trie, NULL, Node as node
from _abcoll import Mapping


class NodeS(node):
    __slots__ = ('value', 'children', 'show')

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
            if node.value is not NULL and node.show: #I added this extra check 'node.show' to hide the combined IP's
                key = "Prefix: " + str(binTools.key_to_prefix(key_factory(parts))) + \
                    '-' + str(node.value[0]) + "  AS " + str(node.value[1])
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

    def update(*args, **kwds):
        ''' D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
            If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
            If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
            In either case, this is followed by: for k, v in F.items(): D[k] = v
        '''
        if not args:
            raise TypeError("descriptor 'update' of 'MutableMapping' object "
                            "needs an argument")
        self = args[0]
        args = args[1:]
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' %
                            len(args))
        if args:
            other = args[0]
            if isinstance(other, Mapping):
                for key in other:
                    self[key] = NodeS
                    self[key].value = other[key]
                    # The auto-generated children's
                    dchildlist = getDefaultChild(key)
                    rchildlist = list()  # The real children Node's from the Trie
                    for child in dchildlist:
                        # Check if the supposed Child is in the SubTrie under
                        # the parent.
                        # The node of each child if there exists such.
                        ckey = self._find(child)
                        # The node of the inserted key.
                        nkey = self._find(key)
                        # To check if the child exist's and AS's match.

                        if ckey is None:
                            break
                        if ckey.value is NULL:
                            break
                        if ckey.value[1] != nkey.value[1]:
                            break
                        rchildlist += [ckey]
                    if len(rchildlist) == len(dchildlist):

                        for child in rchildlist:
                            child.show = False

                        nkey.show = True
                        # I'm just updating the maxLength of the Prefix.
                        nkey.value = [minML(rchildlist),
                                      rchildlist[0].value[1]]
            elif hasattr(other, "keys"):
                for key in other.keys():
                    print "@@@@@@@@@@@@@2This is my IP :", binTools.key_to_prefix(key)
                    self[key] = NodeS
                    self[key].value = other[key]
            else:
                for key, value in other:
                    print "#############This is my IP :", binTools.key_to_prefix(key)
                    self[key] = NodeS
                    self[key].value = other[key]
        for key, value in kwds.items():
            print "$$$$$$$$$$$$$$$$This is my IP :", binTools.key_to_prefix(key)
            self[key] = NodeS
            self[key].value = other[key]

    def __getitem__(self, key):
        node = self._find(key)
        if node is None or node.value is NULL:
            raise KeyError
        return node


def getDefaultChild(key):
    ''' This will auto-generate the supposed children of a prefix.'''
    l = list()
    l += [key + '0']
    l += [key + '1']
    return l


def minML(childList):
    ''' This method should return back the min of the children maxLength'''
    numlist = list()
    for child in childList:
        numlist += [child.value[0]]  # Add the MaxLength to the list
    return min(numlist)
