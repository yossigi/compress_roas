<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 690be4e2456d57b593a80fb8388671e3fb46ec4b
import netaddr

def prefix_to_key(prefix):
    address = prefix.ip.bits().replace(".","")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1
    return "$" + address

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


print ("This is a test: ")
x = prefix_to_key('192.168.0.3')
print x
print key_to_prefix(x)
<<<<<<< HEAD
=======
=======
import netaddr

def prefix_to_key(prefix):
    address = prefix.ip.bits().replace(".","")
    l = int(prefix.cidr.hostmask.bin, 2)
    while(l > 0):
        address = address[:-1]
        l >>= 1
    return "$" + address

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


print ("This is a test: ")
x = prefix_to_key('192.168.0.3')
print x
print key_to_prefix(x)
>>>>>>> 147a9258f8c1d818f9998c6acd800f362e61eae6
>>>>>>> 690be4e2456d57b593a80fb8388671e3fb46ec4b
