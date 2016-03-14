#!/usr/bin/env python3.5
import sys
import time

from myslicelib.util import Endpoint, Credential
from myslicelib.api import Api

from myslicelib import setup as s
from myslicelib.model.resource import Resources, Resource
from myslicelib.model.lease import Leases
from myslicelib.model.slice import Slices, Slice
from myslicelib.model.user import Users, User
from myslicelib.model.authority import Authorities, Authority
from myslicelib.model.project import Projects, Project
from myslicelib.query import q
from pprint import pprint

s.endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
    Endpoint(url="https://194.199.16.164:12346",type="AM"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
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

# users = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get()
# for u in users:
#     print(u) 
#     print(u.authority)
#     print(u.slices)
#     u.slices = []
#     print(u.slices)
#     print(u.pi_authorities)
#     print(u)

auths = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
start_time = time.time()
for auth in auths:
    print('Authority')
    pprint(auth.attributes()) 
    # pprint(auth.users)
    # pprint(auth.projects)
# print(time.time()-start_time)
# auths = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
# for auth in auths:
#     print(auth.id)

proj = q(Project).id('urn:publicid:IDN+onelab:upmc:apitest+authority+sa').get()
for p in proj:
    print('Project')
    pprint(p.attributes())

proj = q(Project).get()
for p in proj:
    print(p.id)


# proj = q(Project).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()

# slices = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()
# for sli in slices:
#     pprint(sli.attributes())
    # pprint(sli.users)
    # pprint(sli.authority)
    # pprint(sli.leases)
    # pprint(sli.resources)

#user = Query(Authority).update('urn:publicid:IDN+onelab:upmc+authority+sa',{'name':'UPMC'})
#user = Query(Authority).update('urn:publicid:IDN+onelab:upmc2+authority+sa',{'name':'UPMC2'})

