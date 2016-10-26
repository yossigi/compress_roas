# compress-ROA's for RPKI-rtr
A python script that wade through the ROAs that rcynic collects and compress it and then output:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```

per line of all the result data.

# How to use:

You need to have these Python packages:
 - Pytrie
 - netaddr

If to be used with rpki-rtr to create a database for the server:

```shell
rpki-rtr cronjob --scan-roas compress-roas [roa-directory] [server/PDU-directory]
```

### if to be used to test performance and compress a set of prefix's, use the experimental branch.

If by its own just to print out the data compressed:

```shell
  compress-roas [roa-directory]
```
