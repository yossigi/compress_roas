

# How to use:

This script just takes a list of prefix's and output the compressed list from the data. 
You can use it for evaluation and stats, it uses the exact compression algorithm.

You need to have these Python packages:

 - Pytrie
 - netaddr

To test a set of prefix's, you can use any of the two styles of input:

## Style 1:
```shell
Format:
Prefix/prefixLen-[maxLength],ASN

Example:
95.187.117.0/24-24,39891
```

 The BGP data-set uses this style of input.
 You can only have 1 prefix per line.
 
## Style 2:
```shell
Format:

timeStamp ASN Prefix1/prefix1Length-[maxLength] [Prefix2]/[prefix2Length]-[prefix2-maxLength] ...

Example:

2016-05-27T11:19:34Z 7020 196.29.128.0/19-24
```
 This style is the one used for ROA's from the RPKI data, you can have multiple prefix's per line, and one ROA per line.

After selecting the Style and the data-set, you just simply run the script.

----
Go to the master branch for how to use with RPKI-rtr tools directly.
