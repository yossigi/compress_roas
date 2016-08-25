def readfile(filename):
    s = set()
    file = open(filename,'r')
    for line in file:
        line = line[1:-1].split()
        st = str(line)
        # print st
        s.add (st)
    return s

s1 = readfile('C:\Users\OSAGGA\Documents\ROA_PyTrie\/test2\/normal_scanner_output.txt')
s2 = readfile('C:\Users\OSAGGA\Documents\ROA_PyTrie\/test2\/Py_prefix_normal.txt')
print len(s1)
print len(s2)

diff = s1.difference(s2)
for ip in diff :
    print ip
# print diff
print len(diff)
