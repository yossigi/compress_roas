# compress_roas
A python script that wades through the ROAs that rcynic collects and compresses them and then outputs:

```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```

per line of all the result data.

# How to use:

You first need to install RPKI.net package (https://github.com/dragonresearch/rpki.net) and then run the following command to fetch the RPKI data using rcynic (https://rpki.net/wiki/doc/RPKI/RP/rcynic), you can use the config sample file included with the package (you may want to edit the download locations of the data).
 ```
 rcynic -c rcynic_config_file
 ```
 - After that you will have the folder 'authenticated', where you can simply pass that folder to compress_roas.py so that it would parse it to get all the ROAs.
 
You also need to have these Python packages:
 - Pytrie
 - netaddr


To use with rpki-rtr to create a database for the server:

```shell
rpki-rtr cronjob --scan-roas compress-roas [roa-directory] [server/PDU-directory]
```

# Reproducing results 
To reproduce the results from "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf) use the "Reproducibility" branch (see README there).
