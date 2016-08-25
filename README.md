# compress-roas for RPKI-rtr
A python script that wade through the ROAs that rcynic collects and compress it and then output:

  [Time] [ASN] [IP_Prefix] [maxLength]

per line of all the result data.

# How to use:

if by it's own just to print out the data commpressed:

  compress-roas [roa-directory]
  
if to be used with rpki-rtr to create a database for the server:

  rpki-rtr cronjob --scan-roas compress-roas [roa-directory] [server-directory]
