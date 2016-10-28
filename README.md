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

#### If to be used to evaluate, reproduce and compress a dataset of prefix's, use the "Reproducibility" branch.

If by its own just to print out the data compressed:

```shell
  compress-roas [roa-directory]
```
