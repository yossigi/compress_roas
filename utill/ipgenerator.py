import netaddr

def key_to_prefix(key):
    k = key
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



def recursive(prefix,length):
    if length == 1 :
        s = '1,' + str(key_to_prefix(prefix)) + '\n'
        f.write(s)
        return
    else:
        f.write('1,' + str(key_to_prefix(prefix)) + '\n')
        recursive(prefix+'0',length - 1)
        recursive(prefix+'1',length - 1)


open('C:\Users\OSAGGA\Documents\ROA_PyTrie\/test.csv','w').close()
f = open('C:\Users\OSAGGA\Documents\ROA_PyTrie\/test.csv','w')
f.write('asn,prefix\n')
recursive('', 16)
f.close()
print 'Done!'
