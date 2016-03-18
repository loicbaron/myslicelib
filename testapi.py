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
    #Endpoint(url="https://194.199.16.164:12346",type="AM"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    #Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

path = "/root/.sfi/"
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

#r = q(Resource).get()
#r = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()
#pprint(r)
# users = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get()
# for u in users:
#     print(u.attributes)
#     print(u.id) 
    # print(u.authority)
    # print(u.slices)
#     u.slices = []
#     print(u.slices)
#     print(u.pi_authorities)
#     print(u)

# u = q(User).id('urn:publicid:IDN+onelab:inria+user+lucia_guevgeozian_odizzio').get().first()

# auths = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
# print('Authority')
# print("attributes")
# pprint(auth.attributes()) 
# #print("users")
# #pprint(auth.users)
# #print("projects")
# #pprint(auth.projects)
# print("pi_users")
# pis = auth.pi_users
# pis.append(u)
# pprint(pis)
# auths.save()

#u = User()
#u.id = 'urn:publicid:IDN+onelab:upmc:apitest+user+zhouquantest'
#pprint(u)
#u.authority = 'onelab.upmc.apitest'
#u.hrn = 'onelab.upmc.apitest.zhouquantest'
#u.email = 'blabla@zhouquantest.com'
#u.keys = ['ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEArj9G7unMu7/zy/WziNMgyBfWGGl+96oEZtH0fXU/ZAnn6SS1S4iaDUjju3EZmXqeu/uYdEQ0pyW3yYNaJoaMzJIseskLV6NgQ70eM/nGDpHIFOobsRSrGyWKHv+tmEMQHLOCq4dGaellv5QR2Ewf+ZnNYw5Rtkgw20tvRRrpuNmzEt4VyK3ayKH/tNvw8EqIpQPdhXAWE/YIRfigDnW3yQdScwImCVyI5wI0MNFAp9IbInRVJscIuHq3ecwv8k7bMGlJlRhjV21wbNfmsY++g8LC3YHQidUH6ISYtAh5COq01VxBrJFVMbye6zAiUONcDLYIZ8OCuRNJxA57qa8Ujw==']
#print(u)
#u.save()
#u.delete()

# u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
# u1 = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
# s = Slice()
# s.authority = 'onelab.upmc'
# s.shortname = 'slice1'
# #s.hrn = 'onelab.upmc.apitest.slice1'
# # s.addUser(u)
# # s.addUser(u1)
# pprint(s)
# #s.resources.append('urn:publicid:IDN+ple:uitple+node+planetlab1.cs.uit.no')
# s.save()

#r = q(Resource).filter('country','Germany').get()
r = q(Resource).filter('country', ['Germany', 'France']).get()
r = q(Resource).filter('country', ['Germany', 'France']).filter('name','plab-vserver').get()
pprint(r)

#r = q(Resource).filter('country','Spain').filter('name','planetlab2.upc.es').get().first()
r = q(Resource).filter('country','Spain').filter('version','f22').get()
u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
u1 = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
s = Slice()
s.authority = 'onelab.upmc'
s.shortname = 'slice1'
#s.hrn = 'onelab.upmc.apitest.slice1'
s.addUser(u)
pprint(s)
s.addUser(u1)
pprint(s)
s.removeUser(u1)
pprint(s)
s.addResources(r)
pprint(s)
##s.resources.append('urn:publicid:IDN+ple:uitple+node+planetlab1.cs.uit.no')
s.save()
pprint(s)

# print(time.time()-start_time)
# auths = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
# for auth in auths:
#     print(auth.id)

#proj = q(Project).id('urn:publicid:IDN+onelab:upmc:apitest+authority+sa').get()
#for p in proj:
#    print('Project')
#    pprint(p.attributes())
#
#proj = q(Project).get()
#for p in proj:
#    print(p.id)


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
=======
>>>>>>> Stashed changes

