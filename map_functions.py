import netaddr

def prefix_to_key(prefix):
    ''' A function given a prefix and AS generates a binary key to be used in a Trie.'''
    if prefix.version == 4:
        address = prefix.ip.bits().replace(".","")
        l = int(prefix.cidr.hostmask.bin, 2).bit_length()
        return str(prefix.version) + "$" + address[:-l]
    elif prefix.version == 6:
        address = prefix.ip.bits().replace(":","")
        l = int(prefix.cidr.hostmask.bin, 2).bit_length()
        return str(prefix.version) + "$" + address[:-l]
    else:
        raise RuntimeError("invalid address version " + str(prefix.version))

def key_to_prefix(key):
    prefix_len_bits = 32
    if key[0] == "#":
        prefix_len_bits = 128
    k = key[1:]
    l = len(k)
    i = 0

    j = 0
    for c in k:
        i <<= 1
        i += int(c)
        j += 1
    i <<= (prefix_len_bits - j)
    ip = netaddr.IPAddress(i)
    return netaddr.IPNetwork(str(ip) + "/" + str(l))
