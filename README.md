# compress_roas
`compress-roas` wades through the ROAs `rcynic` (from RPKI.net, see below) collects and compresses the prefixes based on the prefix length and max length specified in the ROA.
For simplicity, `compress-roas` produces an output with the same format as `scan_roas` (from RPKI.net):
```shell
  [Time] [ASN] [IP_Prefix] [maxLength]
```
`compress-roas` prints A ROA per line.
## Dependencies
Make sure you have the following installed before running `compress-roas`:
- [RPKI.net](https://github.com/dragonresearch/rpki.net/) Relying Party tools.
  - Installation instructions [here](https://github.com/dragonresearch/rpki.net/blob/master/doc/quickstart/xenial-rp.md)
- [Pytrie](https://pypi.python.org/pypi/PyTrie) (you can use `pip` to install this package)
- [netaddr](https://pypi.python.org/pypi/netaddr) (you can use `pip` to install this package)

## How to use:
You can use `compress-roas` with `rpki-rtr`(from RPKI.net) to create a database for an RPKI cache server:
```shell
rpki-rtr cronjob --scan-roas compress-roas [server/PDU-directory]
```
You can also use `compress-roas` on its own (you will need to use it with "sudo" if not used under the user "rpki"):
```shell
compress-roas
```
### Reproducing results 
To reproduce the results from "MaxLength Considered Harmful to the RPKI" (https://eprint.iacr.org/2016/1015.pdf) use the "Reproducibility" branch (see README).
