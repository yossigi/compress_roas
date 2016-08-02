import netaddr

def prefix_to_key(prefix):
    prefix = netaddr.IPNetwork(prefix)
    address = prefix.ip.bits().replace(".","")
    #print '###' + str(address)
    l = int(prefix.cidr.hostmask.bin, 2)
    #print '!!!' + str(l)
    while(l > 0):
        address = address[:-1]
        l >>= 1
    return address

def key_to_prefix(key):
    k = key[1:]
    l = len(k)
    i = 0
    j = 0
    for c in k:
        i <<= 1
        i += int(c)
        j += 1
    i <<= (32 - j)
    ip = netaddr.IPAddress(i)
    return netaddr.IPNetwork(str(ip) + "/" + str(l))
