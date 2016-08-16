#! /usr/bin/python
import netaddr


def prefix_to_key(prefix):
    prefix = netaddr.IPNetwork(prefix)
    #print prefix.version
    address = prefix.ip.bits().replace(".", "").replace(":","")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1
    return '$' + str(prefix.version) + address


def key_to_prefix(key):
    v = int(key[1])
    k = key[2:]
    l = len(k)
    i = 0
    j = 0
    for c in k:
        i <<= 1
        i += int(c)
        j += 1
    i <<= (2**(v+1) - j)
    ip = netaddr.IPAddress(i)
    return netaddr.IPNetwork(str(ip) + "/" + str(l))