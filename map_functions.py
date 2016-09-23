import netaddr


def prefix_to_key(prefix):
    ''' A function given a prefix and AS generates a binary key to be used in a Trie.'''
    prefix = netaddr.IPNetwork(prefix)
    address = prefix.ip.bits().replace(".", "").replace(":","")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1

    # Building the key
    # No need for the first '$', the root is one at the begining.
    key = str(prefix.version) + '$'
    key +=  address
    return key

def key_to_prefix(key):
    ''' A function that given a key from the above function (prefix_to_key) gives back the prefix. '''
    key = key.split('$')
    k = key[3]
    v = int(key[2])
    l = len(k)
    i = 0
    j = 0
    for c in k:
        i <<= 1
        i += int(c)
        j += 1
    if v == 0 :
    	i <<= (32 - j)
    elif v == 1:
    	i <<= (128 - j)
    ip = netaddr.IPAddress(i)
    return netaddr.IPNetwork(str(ip) + "/" + str(l))

# print prefix_to_key('8.8/16',123)
# print key_to_prefix(prefix_to_key('8.8/16',123))
