import subprocess
import time
import datetime
import os, sys

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

[BGP_Config_file, privateKey] = sys.argv[1:3]
# BGP_Config_file = '/home/osagga/Documents/compress-roas/utill/bgpd.conf' # BGP config file location.
# privateKey = '/home/osagga/Documents/compress-roas/utill/orgkeypair.pem'

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

roadata = open('roadata.txt', 'w')
roadata.write(roa_Request)

# print roa_Request



terminal = subprocess.Popen(['openssl', 'dgst', '-sha256', '-sign', privateKey, '-keyform', 'PEM', '-out', 'signature', 'roadata.txt' ], stdout=subprocess.PIPE)
terminal.wait()

terminal = subprocess.Popen(['openssl', 'enc', '-base64', '-in', 'signature', '-out', 'sig_base64'], stdout=subprocess.PIPE)
terminal.wait()


output = '-----BEGIN ROA REQUEST-----\n' + roa_Request + '\n-----END ROA REQUEST-----'+ '\n-----BEGIN SIGNATURE-----\n'+ str(open("sig_base64").read()) + '\n-----END SIGNATURE-----'

print(output)

os.remove('roadata.txt')
os.remove('signature')
os.remove('sig_base64')
