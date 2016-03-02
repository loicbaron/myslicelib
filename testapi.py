#!/usr/bin/env python3.5
import sys
from myslicelib.util import Endpoint, Credential
from myslicelib.api import Api

from myslicelib import setup as s
from myslicelib.model.resource import Resources
from myslicelib.model.lease import Leases
from myslicelib.model.slice import Slices
from myslicelib.model.user import Users, User
from myslicelib.model.authority import Authorities
from myslicelib.query import Query


s.endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
    Endpoint(url="https://194.199.16.164:12346",type="AM"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

path = "/root/.sfi/"
pkey = path + "onelab.upmc.loic_baron.pkey"
hrn = "onelab.upmc.loic_baron"
email = "loic.baron@lip6.fr"
cert = path + "onelab.upmc.loic_baron.user.gid"

#pkey = path + "fed4fire.upmc.loic_baron.pkey"
#hrn = "fed4fire.upmc.loic_baron"
#email = "loic.baron@lip6.fr"
#cert = path + "fed4fire.upmc.loic_baron.user.gid"
#cert = path + "fed4fire.upmc.loic_baron.sscert"


s.credential = Credential(hrn=hrn, email=email, certificate=cert, private_key=pkey)


#lease = Query(Leases).get()
#slices = Query(Slices).get('urn:publicid:IDN+onelab:upmc:test+slice+cloud')
#users = Query(Users).get('urn:publicid:IDN+onelab:upmc+authority+sa')
#user = Query(Users).get('urn:publicid:IDN+onelab:upmc+user+loic_baron')
#authorities = Query(Authorities).get('urn:publicid:IDN+onelab:upmc+authority+sa')
#resource = Query(Resources).get()

user = Query(User).update('urn:publicid:IDN+onelab:upmc+user+loic_baron',{'email':'loic.baron@gmail.com'})

#
#api = Api(s.endpoints, s.credential)
#
# res = api.version()
#
# for k in res['ams']:
#     print("{} : ".format(k))
