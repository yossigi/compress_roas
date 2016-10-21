import subprocess
import time
import datetime

def readfile(filename):
    BGPConf = open(filename,'r')
    prefixSet = set()
    ASN = 0
    for line in BGPConf:
        line = line[:-1].split()
        if 'router' in line and 'bgp' in line:
            ASN = line[2]
        elif 'network' in line and line[0] is not '!':
            prefixSet.add(line[1])
    BGPConf.close()
    return [ASN,prefixSet]

BGP_Config_file = 'C:\Users\OSAGGA\Documents\compress_roas\utill\/bgpd.conf' # BGP config file location.

BGP_data = readfile(BGP_Config_file)
AS = BGP_data[0]
all_prefix = ""
for prefix in BGP_data[1]:
    prefix = prefix.split('/')
    ip = prefix[0]
    length = prefix[1]
    all_prefix += ip + '|' + length + '||'

roa_name = "My First ROA"
time_now = str(int(time.time()))
roa_start_date = str(datetime.datetime.now()).split()[0]
roa_end_date = "mm-dd-yyyy" # Not sure what to put here.

roa_Request = "1|" + time_now + "|" + roa_name + "|" + AS + "|" + roa_start_date + "|"+ roa_end_date+ "|" + all_prefix

# print roa_Request

terminal = subprocess.Popen([['echo', '-n', roa_Request ,'>'], 'roadata.txt' ], stdout=subprocess.PIPE)
output = terminal.communicate()[0]
