This branch has the script used in measuring the RPKI data shown in "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf).

## Dependencies
Make sure you have the following installed before running `compress_roas.py`:
- [RPKI.net](https://github.com/dragonresearch/rpki.net/) Relying Party tools.
  - Installation instructions [here](https://github.com/dragonresearch/rpki.net/blob/master/doc/quickstart/xenial-rp.md)
- [Pytrie](https://pypi.python.org/pypi/PyTrie) (you can use `pip` to install this package)
- [netaddr](https://pypi.python.org/pypi/netaddr) (you can use `pip` to install this package)
 
## Data-sets used:
- BGP RIB files:
  - For the IPv6 you can find the RIB files through here (http://archive.routeviews.org/route-views6/bgpdata/)
  - For the IPv4 you can find the RIB files through here (http://archive.routeviews.org/route-views4/bgpdata/)
  - After you download the RIB file, you would need to use 'libBGPdump' (https://bitbucket.org/ripencc/bgpdump/wiki/Home) to  parse the RIB file you downloaded from the binary format to text format.
   ```
   ./bgpdump RIB_file > output_file.txt
   ```
  - Keep in mind that the output file size is large (around 8 GB)
  - The output format is what you would pass into compress_roas.py as a BGP data-set.
- ROA data folder:
  - You need to make sure that [RPKI.net](https://github.com/dragonresearch/rpki.net/) Relying Party tools are running and fetching data (a fresh installation should be enough to make them run).
  - Run the following command to save the RPKI data to a folder representation using `rcynic-dump`([here](https://github.com/dragonresearch/rpki.net/blob/master/rp/rcynic/rcynic-dump))
   ```
   sudo -u rpki rcynic-dump [authenticated-output-path]
   ```
  - Now that you have the folder 'authenticated' with the RPKI data, you will pass it to compress_roas.py (see below).
  - Due to the unavailability of a public directory with snapshots of the RPKI data history (like BGPView), it might be more convenient to use the RPKI data we uploaded [here](RPKI_dataset/) to reproduce the results.
    - The data is uploaded in ROA list format, so it's recommended to use the second style of using `compress_roas.py` described below to handle the data sets.

## How to use:
Make sure to build "bgp_announcement_parser" before running `compress_roas.py` using the following instructions:
```
cd tools
make 
```

### compress_roas.py
Takes as input the path to the RPKI 'authenticated' directory, and may also take multiple paths to BGP RIB (text-format) files to reproduce the results.
```
compress_roas.py ROA-data-folder [BGP_data_set1, BGP_data_set2, ..]
```
`compress_roas.py` can also take a list of ROAs `ROA-list.txt` (ROAs should have the same format that `scan_roas` produces ([here](https://github.com/yossigi/compress_roas#compress_roas)), one per line, saved in a `txt` file) as an input to provide more portability.
```
compress_roas.py ROA-list.txt [BGP_data_set1, BGP_data_set2, ..]
```

***
### tools/bgp_announcement_parser.cpp
This script takes in as an input the BGP RIB in the text format (the output of 'bgpdump') and parses it such that it generates an output file will all of the BGP announcements as follows:
```
prefix1/prefix1Len-prefix1Len,ASN1
prefix2/prefix2Len-prefix2Len,ASN2
.
.
```
***
### tools/scan_roas.py
`scan_roas` (from [RPKI.net](https://github.com/dragonresearch/rpki.net/blob/b2eee832ae27af6ea82f412ee304a778b0910851/doc/manual/36.RPKI.Utils.md#scan_roas) tools) searches the authenticated database of RPKI ROA objects that rcynic creates, and prints out the signing time, ASN, and prefixes for each ROA, one ROA per line.
```
sudo -u rpki scan_roas [-h | --help] [rcynic_directory]
```
***
### valid_announcements.py
This script has the function 'save_valid_announcements_to_file' that takes in a BGP announcements file (the output of 'bgp_announcement_parser') and a ROA list file (the output of 'scan_roas') and then outputs a list of the prefixes that appear in the BGP announcements and are mentioned in a ROA from the list of ROAs (so that the prefix is valid).

# Reproduction

To reproduce all the scenarios in Section 6, summarized in Table 1 of the paper. First we need to have the datasets with the desired date, then we run the following command:

- If the RPKI data is in the dump "format", we use the following: 
```
compress_roas.py ROA-data-folder [BGP_data_set1, BGP_data_set2, ..]
```
- If the RPKI data is in a list format (specified above), we use the following:
```
compress_roas.py ROA-list.txt [BGP_data_set1, BGP_data_set2, ..]
```
The output will point out to each specific scenario, and where to find it in Table.1 from the paper.

----
Go to the master branch for how to use with RPKI-rtr tools directly.
