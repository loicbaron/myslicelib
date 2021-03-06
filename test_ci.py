#!/usr/bin/env python3.5
import sys
import os
from myslicelib.util import Endpoint, Authentication
from myslicelib.api import Api

from myslicelib import setup as s
from myslicelib.model.resource import Resources
from myslicelib.model.lease import Leases
from myslicelib.model.slice import Slices, Slice
from myslicelib.model.user import Users, User
from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q


s.endpoints = [
    #Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
    #Endpoint(url="https://194.199.16.164:12346",type="AM"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    #Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

path = "/root/"

print 
pkey = path + "myslice.pkey"
hrn = "onelab.myslice"
email = "support@myslice.info"
cert = path + "myslice.cert"

#pkey = path + "lbaron.pkey"
#hrn = "onelab.upmc.lbaron"
#email = "loic.baron@gmail.com"
#cert = path + "onelab.upmc.lbaron.user.gid"


#pkey = path + "fed4fire.upmc.loic_baron.pkey"
#hrn = "fed4fire.upmc.loic_baron"
#email = "loic.baron@lip6.fr"
#cert = path + "fed4fire.upmc.loic_baron.user.gid"
#cert = path + "fed4fire.upmc.loic_baron.sscert"


s.authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)


#lease = Query(Leases).get()
#slices = Query(Slices).get('urn:publicid:IDN+onelab:upmc:test+slice+cloud')
#authorities = Query(Authorities).get('urn:publicid:IDN+onelab:upmc+authority+sa')
#resource = Query(Resources).get()

users = q(User).get()
print(users)

users = q(User).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
print(users)

user = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get()
print(user)

user = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({'email':'loic.baron@gmail.com'})
print(user)

user = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({'email':'loic.baron+5@gmail.com'})
print(user)

user = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').delete()
print(user)

#authority = Query(Authority).update('urn:publicid:IDN+onelab:upmc2+authority+sa',{})
#authority = Query(Authority).get('urn:publicid:IDN+onelab:upmc2+authority+sa')
#authority = Query(Authority).delete('urn:publicid:IDN+onelab:upmc2+authority+sa')

authority = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
print(authority)
#authority.pis()

# users and resources must be defined for AM
#slices = q(Slice).update('urn:publicid:IDN+onelab:upmc+slice+toto',{})
#slices = Query(Slices).get('urn:publicid:IDN+onelab:upmc+slice+toto')
#slices = Query(Slices).delete('urn:publicid:IDN+onelab:upmc+slice+toto')

#slices = q(Slice).get('urn:publicid:IDN+onelab:upmc+slice+toto')
#slices = Query(Slices).get()
#slices = q(Slice).get('urn:publicid:IDN+onelab:upmc+authority+sa')

#slice = Query(Slice).update('urn:urn:publicid:IDN+onelab:upmc+slice+testing_loic')

#user = Query(Authority).update('urn:publicid:IDN+onelab:upmc+authority+sa',{'name':'UPMC'})
#user = Query(Authority).update('urn:publicid:IDN+onelab:upmc2+authority+sa',{'name':'UPMC2'})

#
#api = Api(s.endpoints, s.authentication)
#
# res = api.version()
#
# for k in res['ams']:
#     print("{} : ".format(k))
