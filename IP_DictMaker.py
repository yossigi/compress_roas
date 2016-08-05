import map_functions as binTools

def getDict(filename):
    IPdict = dict()
    file = open(filename, 'r')
    for line in file:
        ip = line[:-1].split(',')
        # Update the Dict.
        IPdict.update(ipReady(ip[0].strip(), ip[1].strip()))
    file.close()
    return IPdict

def ipReady(prefix, AS):
    key = binTools.prefix_to_key(prefix)
    maxLength = len(key) -1
    AS = int(AS)
    return {key: [maxLength, AS]}
