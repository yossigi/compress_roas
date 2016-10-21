# compress-roas for RPKI-rtr
A python script that wade through the ROAs that rcynic collects and compress it and then output:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
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
# ROA-Requester

A python script given the directory of the BGP config and private key should genarate a ROA request.
```shell
  roa-requester [bgp-config-file-directory] [privateKey-directory]
```
