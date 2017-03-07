
filen = open('C:\Users\osagg\Documents\ROA_PyTrie\Data files\semi_dup.txt','r')
s = set()
for line in filen:
    line = line[:-1]
    if line in s:
        print line
    else:
        s.add(line)
