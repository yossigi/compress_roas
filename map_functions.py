#! /usr/bin/python
import netaddr


def prefix_to_key(prefix, AS):
    prefix = netaddr.IPNetwork(prefix)
    #print prefix.version
    address = prefix.ip.bits().replace(".", "").replace(":","")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1
    if prefix.version == 4:
	return '$' + str(0) + str(bin(AS))[2:] + '$' +  address
    elif prefix.version == 6:
	return '$' + str(1) + str(bin(AS))[2:] + '$' +  address


def key_to_prefix(key):
    v = int(key[1])
    k = key.split('$')[2]
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

# print prefix_to_key('192.168.1.1/16',123)
