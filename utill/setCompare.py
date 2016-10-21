''' Just to compare two sets of data. '''


def readfile(filename):
    s = set()
    file = open(filename,'r')
    for line in file:
        line = line[1:-1].split()
        st = str(line)
        # print st
        s.add (st)
    return s

Filename1 = ''
Filename2 = ''
s1 = readfile(Filename1)
s2 = readfile(Filename2)

print len(s1)
print len(s2)

diff = s1.difference(s2)
for ip in diff :
    print ip
# print diff
print len(diff)
