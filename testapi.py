#!/usr/bin/env python3.5
import sys
from myslicelib.util import Endpoint, Credential
from myslicelib.api import Api

from myslicelib import setup as s
from myslicelib.model.resource import Resources, Resource
from myslicelib.model.lease import Leases
from myslicelib.model.slice import Slices, Slice
from myslicelib.model.user import Users, User
from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q
from pprint import pprint

s.endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
    Endpoint(url="https://194.199.16.164:12346",type="AM"),
    Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    #Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

# path = "/root/.sfi/"
# pkey = path + "onelab.upmc.loic_baron.pkey"
# hrn = "onelab.upmc.loic_baron"
# email = "loic.baron@lip6.fr"
# cert = path + "onelab.upmc.loic_baron.user.gid"

path = "/root/.sfi/"
pkey = path + "onelab.upmc.joshzhou16.pkey"
cert = path + "onelab.upmc.joshzhou16.sscert"

hrn = "onelab.upmc.joshzhou16"
email = "joshzhou16@gmail.com"


#pkey = path + "lbaron.pkey"
#hrn = "onelab.upmc.lbaron"
#email = "loic.baron@gmail.com"
#cert = path + "onelab.upmc.lbaron.user.gid"


#pkey = path + "fed4fire.upmc.loic_baron.pkey"
#hrn = "fed4fire.upmc.loic_baron"
#email = "loic.baron@lip6.fr"
#cert = path + "fed4fire.upmc.loic_baron.user.gid"
#cert = path + "fed4fire.upmc.loic_baron.sscert"


s.credential = Credential(hrn=hrn, email=email, certificate=cert, private_key=pkey)


#lease = Query(Leases).get()
#slices = Query(Slices).get('urn:publicid:IDN+onelab:upmc:test+slice+cloud')
#authorities = Query(Authorities).get('urn:publicid:IDN+onelab:upmc+authority+sa')
#resource = Query(Resources).get()

# users = q(User).get()
# print(users)

# users = q(User).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
# print(users)

# user = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get()
# print(user)

# user = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({'email':'loic.baron@gmail.com'})
# print(user)

# user = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({'email':'loic.baron+5@gmail.com'})
# print(user)

# user = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').delete()
# print(user)

#authority = Query(Authority).update('urn:publicid:IDN+onelab:upmc2+authority+sa',{})
#authority = Query(Authority).get('urn:publicid:IDN+onelab:upmc2+authority+sa')
#authority = Query(Authority).delete('urn:publicid:IDN+onelab:upmc2+authority+sa')

users = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get()
for u in users:
    print(u) 
    print(u.authority)
    print(u.slices)
    u.slices = []
    print(u.slices)
    print(u.pi_authorities)
    print(u)

# auths = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
auths = q(Authority).id('urn:publicid:IDN+onelab:upmc:apitest+authority+sa').get()
for auth in auths:
    pprint(auth) 
    pprint(auth.users)


#authority = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
#print(authority)
#authority.pis()


# users and resources must be defined for AM
#slices = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()
#pprint(slices)


#slices = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+authority+sa').get()
#pprint(slices)

#slices = Query(Slices).delete

#slices = q(Slice).get('urn:publicid:IDN+onelab:upmc+slice+toto')
#slices = Query(Slices).get()
#slices = q(Slice).get('urn:publicid:IDN+onelab:upmc+authority+sa')

#slice = Query(Slice).update('urn:urn:publicid:IDN+onelab:upmc+slice+testing_loic')

#user = Query(Authority).update('urn:publicid:IDN+onelab:upmc+authority+sa',{'name':'UPMC'})
#user = Query(Authority).update('urn:publicid:IDN+onelab:upmc2+authority+sa',{'name':'UPMC2'})

#
#api = Api(s.endpoints, s.credential)
#
# res = api.version()
#
# for k in res['ams']:
#     print("{} : ".format(k))
