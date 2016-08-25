import netaddr

'''This program genarates a list of all the possible IP prefix's to a limit of your choice. '''
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

Filename = 'Where\to\save\the\output\'

open('Filename','w').close() # to reset the file everytime you run the code.
f = open(Filename,'w')
f.write('asn,prefix\n') # The first line, you can delete this if not needed.
prefix_limit = 16 # The limit to stop after reaching.
recursive('', prefix_limit)
f.close()
print 'Done!'
