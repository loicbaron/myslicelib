#!/usr/bin/env python3.5
import os

pkey = os.environ['MYSLICE_PKEY']
text_file = open("/root/myslice.pkey", "w")
text_file.write(pkey)
text_file.close()

cert = os.environ['MYSLICE_CERT']
text_file = open("/root/myslice.cert", "w")
text_file.write(cert)
text_file.close()
