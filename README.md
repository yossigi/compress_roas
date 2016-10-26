# How to use:

This script just takes a list of prefix's and output the compressed list from the data. 
You can use it for evaluation and stats, it uses the exact compression algorithm.

You need to have these Python packages:

 - Pytrie
 - netaddr

To test a set of prefix's, You have two Styles of input, Max-Length is optional in both styles:

## Style 1:
```shell
[Prefix]/[prefix-len]-[max-len],[ASN]
```

 The BGP data-set uses this style of input.
 You can only have 1 prefix per line.
 
## Style 2:
 ```shell
[ROA time-stamp] [ASN] [Prefix1]/[prefix1-len]-[max-len] [Prefix2]/[prefix2-len]-[max-len] ...
```
 This style is the one used for ROA's from the RPKI data, you can have multiple prefix's per line, and one ROA per line.

After selecting the Style and the data-set, you just simply run the script.

----
Go to the master branch for how to use with RPKI-rtr tools directly.
