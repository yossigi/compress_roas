# compress-roas for RPKI-rtr
A python script that wade through the ROAs that rcynic collects and compress it and then output:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```

per line of all the result data.

# How to use:

You need to have these Python pacakges:
 - Pytrie
 - netaddr

if to be used with rpki-rtr to create a database for the server:

```shell
rpki-rtr cronjob --scan-roas compress-roas [roa-directory] [server-directory]
```

### if to be used to test preformance and comprese a set of prefix's, use the [name] branch.

if by it's own just to print out the data commpressed:

```shell
  compress-roas [roa-directory]
```
