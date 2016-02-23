#!/usr/bin/env python3.5
import sys
from myslicelib.api import Endpoint, Credential
from myslicelib.api import Api

from myslicelib import setup as s
from myslicelib.model.resource import Resources
from myslicelib.query import Query


s.endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    #Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

path = "/Users/moray/Sites/upmc/"
pkey = path + "cscognamiglio_onelab.pkey"
hrn = "onelab.upmc.cscognamiglio"
email = "cscognamiglio@gmail.com"
cert = path + "cscognamiglio_onelab.cert"

s.credential = Credential(hrn=hrn, email=email, certificate=cert, private_key=pkey)


resources = Query(Resources).get()




#
#api = Api(s.endpoints, s.credential)
#
# res = api.version()
#
# for k in res['ams']:
#     print("{} : ".format(k))
