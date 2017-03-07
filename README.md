# compress-ROA's for RPKI-rtr
A python script that wade through the ROAs that rcynic collects and compress it and then output:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```

per line of all the result data.

# How to use:

You need to have these Python packages:
 - RPKI Toolkit (https://github.com/dragonresearch/rpki.net)
 - Pytrie
 - netaddr

To use with rpki-rtr to create a database for the server:

```shell
rpki-rtr cronjob --scan-roas compress-roas [roa-directory] [server/PDU-directory]
```

# Reproducing results 
To reproduce the results from "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf) use the "Reproducibility" branch (see README.md there).
