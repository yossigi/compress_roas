# compress_roas
A python script that wades through the ROAs that rcynic collects and compresses them and then outputs:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```

per line of all the result data.

# Dependencies
- You first need to install RPKI.net package (https://github.com/dragonresearch/rpki.net/) and have it running and fetching ROAs.
- You also need to have these Python packages:
 - Pytrie
 - netaddr

# How to use:
You can use the script with rpki-rtr to create a database for the server:
```shell
rpki-rtr cronjob --scan-roas compress-roas [server/PDU-directory]
```
Or you can just use it on its own (you might need to use it with "sudo" since it requests access to the user "rpki":
```shell
compress-roas
```
# Reproducing results 
To reproduce the results from "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf) use the "Reproducibility" branch (see README there).
