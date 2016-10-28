This branch has the data-sets used in "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf) and below are the instructions on how to reproduce the results provided in the paper. 

### The data-sets located in the "Data_files" folder:
- "bgp_announcements.txt" corresponds to "Full deployment, minimal ROAs, with maxLenth" scenario
- "bgp_valid_announcements.txt" corresponds to "Today, minimal ROAs, no maxLength" scenario
- "roa_list.txt" corresponds to "Today’s RPKI" scenario


# How to use:

The script takes a data-set of prefix's and outputs the compressed list of the data-set. 
You can use it for evaluation and reproducibility, it uses the exact compression algorithm as the script in master.

In order to run the script, you need to have these Python packages installed:

 - Pytrie
 - netaddr

To compress a data-set, you can use any of these two format-styles of input:

## Style 1:
```shell
Format:
Prefix/prefixLen-[maxLength],ASN

Example:
95.187.117.0/24-24,39891
```

Both "bgp_announcements.txt" and "bgp_valid_announcements.txt" have this style of input.
 You can only have 1 prefix per line.
 
## Style 2:
```shell
Format:

timeStamp ASN Prefix1/prefix1Length-[maxLength] [Prefix2]/[prefix2Length]-[prefix2-maxLength] ...

Example:

2016-05-27T11:19:34Z 7020 196.29.128.0/19-24
```
"roa_list.txt" have this style of input, you can have multiple prefix's within a line line, and one ROA per line.


After selecting the data-set with the correct style (commenting out the files not used in the script):

```shell
IPfilenameS_1 = os.path.abspath("Data_files/bgp_valid_announcements.txt")
# IPfilenameS_1 = os.path.abspath("Data_files/bgp_announcements.txt")
IPfilenameS_2 = os.path.abspath("Data_files/roa_list.txt")

# You switch between these two depending on the format of your input

# Trie_Dict = getStyle_1(IPfilenameS_1)
Trie_Dict = getStyle_2(IPfilenameS_2)
```

simply run the script.

----
Go to the master branch for how to use with RPKI-rtr tools directly.
