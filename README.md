This branch has the data-sets used in "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf) and below are the instructions on how to reproduce the results provided in the paper and/or run them on new datasets.


### Data-sets used:
- BGP RIB files:
 - For the IPv6 you can find the RIB files through here (http://archive.routeviews.org/route-views6/bgpdata/)
 - For the IPv4 you can find the RIB files through here (http://archive.routeviews.org/route-views4/bgpdata/)
 - After you download the RIB file, you would need to use 'libBGPdump' (https://bitbucket.org/ripencc/bgpdump/wiki/Home) to  parse the RIB file you downloaded from the binary format to text format.
 ```
 ./bgpdump RIB_file > output_file.txt
 ```
 - The output format is what you would pass into compress_roas.py as a BGP data-set.
- ROA data folder:
 - You first need to install RPKI.net package (https://rpki.net/wiki/doc/RPKI/Installation)
   - Make sure to install the one from this link since the Github version has sligtily diffrent output format.
 - Run the following command to fetch the RPKI data using rcynic (https://rpki.net/wiki/doc/RPKI/RP/rcynic), you can use the config sample file included with the package (you may want to edit the download locations of the data).
 ```
 rcynic -c rcynic_config_file
 ```
 - After you have the folder 'authenticated', you can simply pass that folder to compress_roas.py so that it would parse it to get all the ROAs.

# How to use:

## compress_roas
It takes as input the path to the RPKI 'authenticated' directory, and may also take mutiple paths to BGP RIB (text-format) files to reproduce our results as we explain in the following section.

In order to run the script, you need to have these Python packages installed:

 - Pytrie
 - netaddr

Then you would need to build the "bgp_announcement_parser" using the following command:
```
cd tools
make 
```
Then you would use compress_roas.py as follows:
```
compress_roas.py ROA-data-folder [BGP_data_file1, BGP_data_file2, ..]
```
***
## tools/bgp_announcement_parser.cpp
This script takes in as an input the BGP RIB in the text format (the output of 'bgpdump') and parse it such that it generates an output file with only the prefixs anounced with thier ASN as follows:
```
prefix1/prefix1Len-prefix1Len,ASN1
prefix2/prefix2Len-prefix2Len,ASN2
.
.
```
***
## tools/scan_roas.py
scan_roas searchs the authenticated result tree from an rcynic run for ROAs, and prints out the signing time, ASN, and prefixes for each ROA, one ROA per line.
Full documentation can be found here (https://rpki.net/wiki/doc/RPKI/Utils#scan_roas)
***
## valid_announcements.py
This script has the function 'save_valid_announcements_to_file' that takes in a BGP announcements file (the output of bgp_announcement_parser) and a ROA list file (the output of 'scan_roas') and then outputs a list of the prefixs that appear in the BGP annoncments and are mentioned in a ROA (so they are valid).

# Reproduction

To reproduce all the senarios in Section 6, summraized in Table 1 of the paper. We would run the following command:
```
compress_roas.py ROA-data-folder [BGP_data_file1, BGP_data_file2, ..]
```
The output will point out to each specific senario, and where to find it in Table.1

----
Go to the master branch for how to use with RPKI-rtr tools directly.
