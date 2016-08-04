import netaddr


def prefix_to_key(prefix):
    prefix = netaddr.IPNetwork(prefix)
    address = prefix.ip.bits().replace(".", "")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1
    return address


def key_to_prefix(key):
    #k = key[1:]
    l = len(key)
    i = 0
    j = 0
    for c in key:
        i <<= 1
        i += int(c)
        j += 1
    i <<= (32 - j)
    ip = netaddr.IPAddress(i)
    return netaddr.IPNetwork(str(ip) + "/" + str(l))
