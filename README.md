# compress-roas for RPKI-rtr
A python script that wade through the ROAs that rcynic collects and compress it and then output:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```
# ROA-Requester

```shell
  roa-requester [bgp-config-file-directory] [privateKey-directory]
```


per line of all the result data.

# How to use:

if to be used with rpki-rtr to create a database for the server:

```shell
rpki-rtr cronjob --scan-roas compress-roas [roa-directory] [server-directory]
```
  
if by it's own just to print out the data commpressed:

```shell
  compress-roas [roa-directory]
```
