#!/usr/bin/env python3.5
import os, sys, time

from myslicelib.util import Endpoint, Authentication
from myslicelib.api import Api

from myslicelib import setup as s, Setup
from myslicelib.model.resource import Resources, Resource
from myslicelib.model.lease import Leases, Lease
from myslicelib.model.slice import Slices, Slice
from myslicelib.model.user import Users, User
from myslicelib.model.testbed import Testbed
from myslicelib.model.authority import Authorities, Authority
from myslicelib.model.project import Projects, Project
from myslicelib.query import q
from pprint import pprint

s.endpoints = [
    #Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM", name="ple"),
    #Endpoint(url="https://194.199.16.164:12346",type="AM", name="iotlab"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM",name="WiLab.t"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg", name="OneLab Reg"),
    #Endpoint(url="https://localhost:12345",type="Reg", name="OneLab Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

path = os.path.expanduser("~/.sfi/")
pkey = path + "onelab.upmc.loic_baron.pkey"
hrn = "onelab.upmc.loic_baron"
email = "loic.baron@lip6.fr"
cert = path + "onelab.upmc.loic_baron.user.gid"
# expired cred
credentials = None
#credentials = [{'user_credential':path+'onelab.upmc.loic_baron.user_for_onelab.myslice.user.cred'}
#credentials = [{'user_credential':path+'onelab.upmc.loic_baron.user.cred'}
#credentials = [
#              {'type':'user', 'hrn':'onelab.upmc.loic_baron', 'xml':path+'onelab.upmc.loic_baron.user.cred'},
#              #{'id':'xxxx', 'xml':path+'onelab.upmc.loic_baron.user.cred'},
#              {'type':'slice', 'hrn':'onelab.upmc.slice1', 'xml':path+'onelab.upmc.loic_baron-onelab.upmc.slice1.slice.cred'},
#              {'type':'authority', 'hrn':'onelab.upmc', 'xml':path+'onelab.upmc.loic_baron-onelab.upmc.authority.cred'},
#              ]



#pkey = path + "lbaron.pkey"
#hrn = "onelab.upmc.lbaron"
#email = "loic.baron@gmail.com"
#cert = path + "onelab.upmc.lbaron.user.gid"

#pkey = path + "fed4fire.upmc.loic_baron.pkey"
#hrn = "fed4fire.upmc.loic_baron"
#email = "loic.baron@lip6.fr"
#cert = path + "fed4fire.upmc.loic_baron.user.gid"
#cert = path + "fed4fire.upmc.loic_baron.sscert"

s.authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey, credentials=credentials)

#print("Leases in AMs")
#l = q(Lease).get()
#pprint(l)

r = q(Resource).get().first()

import time
u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
pprint(u)
print("Get Slice")
s = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicetest').get().first()
pprint(s)
l = Lease()
l.slice_id = s.id
l.start_time = int(time.time())
l.duration = 3600
#l.end_time = 1458324000
# XXX In builder check that resources belong to the right testbed
l.addResource(r)
pprint(l)
s.addLease(l)
s.addResource(r)
pprint(s)
s = s.save()
pprint(s)
exit(1)

s = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicetest').get().first()
pprint(s1)
exit(1)
t = q(Testbed).get()
pprint(t)
#l = q(Lease).get()
#pprint(l)

u = q(User).get()
pprint(u)
u = q(Authority).get()
pprint(u)

exit(1)

u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
pprint(u)
u.getCredentials()
pprint(u)
u.getCredentials(delegate_to="onelab.myslice")
pprint(u)
exit(1)

v = q(User).get()
#v = q(Testbed).filter('name','iotlab').get()
pprint(v)
exit(1)

u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
print(u.id)
# Quite long to Query AMs
#sl = u.getSlices()
#pprint(sl)
sl = u.slices
pprint(sl)
exit(1)
p1 = q(Project).id('urn:publicid:IDN+onelab:upmc:z2+authority+sa').get().first()
print(p1.id)
exit(1)
p1 = q(Project).id('urn:publicid:IDN+onelab:upmc:z2+authority+sa').get()
pprint(p1)

p = Project()
p.id = 'urn:publicid:IDN+onelab:upmc:z8+authority+sa'
p.authority = 'urn:publicid:IDN+onelab:upmc:z8+authority+sa'
pprint(p)
#ret = p.save()
#pprint(ret)
#pprint(p)
exit(1)
print("7 - GET resources in Spain")
resources = q(Resource).filter('country','Spain').get()
pprint(resources)
exit(1)
print("1. GET User")
u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
pprint(u)
exit(1)
u.getCredentials()
u.getCredentials(delegate_to="onelab.myslice")
pprint(u)
exit(1)
#print("1 - GET Slice")
#s1 = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+s1').get().first()
#pprint(s1)
#print("2 - GET User & ADD to Slice")
print("GET User")
u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
#s1.addUser(u)
#pprint(s1)
#print("3 - Save Slice")
#s1.save()
print("4 - GET Slice")
s2 = q(Slice).id('urn:publicid:IDN+onelab:upmc:apitest+slice+s1').get().first()
#pprint(s2)
#print("5 - REMOVE User from Slice")
#s2.removeUser(u)
#pprint(s2)
#print("6 - Save Slice")
#s2.save()
#pprint(s2)

print("7 - GET resources in Spain")
resources = q(Resource).filter('country','Spain').get()
pprint(resources)
print("8 - ADD resources to Slice & Save")
s2.addResources(resources)
s2.save()
print("9 - REMOVE resources from Slice & Save")
for r in resources:
    if r.name not in ['planetlab1.tlm.unavarra.es','planetlab2.tlm.unavarra.es']:
        s2.removeResource(r)
s2.save()
pprint(s2)
exit(1)
#a = q(Authority).id('urn:publicid:IDN+onelab:toto+authority+sa').get().first()
#pprint(a)
#a = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get().first()
#pprint(a)
#a = Authority()
#a.hrn = "onelab.toto"
#a.save()
#pprint(a)

#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
#pprint(u)
#
#user_setup = Setup()
#user_setup.endpoints = [
#    #Endpoint(url="https://localhost:12345",type="Reg", name="OneLab Reg"),
#    Endpoint(url="https://portal.onelab.eu:6080",type="Reg", name="OneLab Reg"),
#]
#path = "/root/.sfi/"
#pkey = path + "onelab.upmc.joshzhou16.pkey"
##cert = path + "onelab.upmc.joshzhou16.sscert"
#cert = path + "onelab.upmc.joshzhou16.user.gid"
#hrn = "onelab.upmc.joshzhou16"
#email = "joshzhou16@gmail.com"
#credentials = None
#user_setup.authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey, credentials=credentials)
#
#creds = u.getCredentials(setup=user_setup)
#print("-"*20)
#pprint(u)
#exit(1)
#a = q(Resource).get()
#pprint(a)
#a = q(Lease).get()
#pprint(a)
#res = q(User).id('urn:publicid:IDN+onelab:inria+user+lbaron').update({'email':'loic.baron@gmail.com'})
#pprint(res)
#res = q(User).id('urn:publicid:IDN+onelab:inria+user+lbaron').delete()
#pprint(res)

#p = Project()
#p.id = 'urn:publicid:IDN+onelab:u:infocom+authority+sa'
##p.addPi(u)
#ret = p.save()
#pprint(ret)

#u = q(User).get()
#pprint(u)
#
#r = q(Resource).get()
#pprint(r)
#pprint(r.logs)

# XXX Don't use Filter!!! 
# it is not optimal, as it is doing List and then Resolve for each element...
#a = q(Authority).filter('hrn','onelab.upmc').get()
#a = q(Authority).get()
#a = q(Project).get()
#a = q(Authority).get()
#pprint(a)
#a = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get().first()
#pprint(a)
#a = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get().first()
#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
#u_a = a.isPi(u)
#print(u_a)
#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
#u_a = a.isPi(u)
#print(u_a)

#p = q(Project).filter('hrn','onelab.upmc.infocom').get()
#pprint(p)
#p = q(Project).id('urn:publicid:IDN+onelab:upmc:infocom+authority+sa').get().first()
#pprint(p)
#exit(1)
#x = p.getAuthority()
#
#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
#u_p = p.isPi(u)
#print(u_p)
#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
#u_x = x.isPi(u)
#print(u_x)
#
#pprint(x)

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

#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
u = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
u.getCredentials()
#u.getCredentials("onelab.myslice")
pprint(u)
#s = Slice()
#s.authority = 'onelab.upmc'
#s.shortname = 'slice1'
###s.hrn = 'onelab.upmc.apitest.slice1'
#s.addUser(u1)
#s.removeUser(u)
#s.save()
#pprint(s)

#r = q(Resource).filter('country','Germany').get()
#r = q(Resource).filter('country', ['Germany', 'France']).get()
#r = q(Resource).filter('country', ['Germany', 'France']).filter('name','plab-vserver').get()

#ls = q(Lease).get()
#pprint(ls)

#s1 = q(Slice).id("urn:publicid:IDN+onelab:upmc+slice+slice1").get()
#pprint(s1)
#s1 = q(Slice).filter('authority','urn:publicid:IDN+onelab:upmc+authority+sa').get()
#pprint(s1)
#s1 = q(Slice).get()
#pprint(s1)

#r = q(Resource).filter('name', 'wsn430-27.grenoble.iot-lab.info').get()
#pprint(r)
#r1 = q(Resource).filter('country','Spain').filter('name','planetlab2.upc.es').get()
#pprint(r1)
#r.update(r1)

d1 = {'available': 'true', 'id': 'urn:publicid:IDN+iotlab+node+wsn430-27.grenoble.iot-lab.info', 'technologies': ['IoT', 'Internet of Things'], 'hardware_types': ['wsn430:cc1101'], 'name': 'wsn430-27.grenoble.iot-lab.info', 'type': 'node', 'sliver_types': [], 'interfaces': [], 'parser': 'iotlab', 'manager': 'urn:publicid:IDN+iotlab+authority+sa', 'location': {'country': 'France'}, 'exclusive': 'true'}
r1 = Resource(d1)

d2 = {'available': 'false', 'id': 'urn:publicid:IDN+ple:upcple+node+planetlab2.upc.es', 'location': {'longitude': '2.11273', 'latitude': '41.3897', 'country': 'Spain'}, 'technologies': ['Virtual Machines', 'Distributed Systems', 'Internet', 'Wired'], 'services': [], 'hardware_types': ['plab-pc', 'pc'], 'name': 'planetlab2.upc.es', 'type': 'node', 'interfaces': ['urn:publicid:IDN+ple+interface+node931:eth0'], 'parser': 'ple', 'manager': 'urn:publicid:IDN+ple+authority+cm', 'sliver_types': [{'name': 'plab-vserver', 'disk_images': [{'name': 'Fedora f22', 'version': 'f22', 'os': 'Linux'}]}], 'exclusive': 'false'}
r2 = Resource(d2)

r = [r1,r2]

##r = q(Resource).filter('country','Spain').filter('version','f22').get()
#u = q(User).id('urn:publicid:IDN+onelab:upmc+user+joshzhou16').get().first()
#u1 = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
#pprint(u)

#p = q(Project).get()

#s = Slice()
#s.authority = 'onelab.upmc'
#s.shortname = 'slice1'
###s.hrn = 'onelab.upmc.slice1'
#s.addUser(u)
##pprint(s)
#s.addUser(u1)
##pprint(s)
##s.removeUser(u1)
##pprint(s)
### XXX In builder check that resources belong to the right testbed
#s.addResources(r)
##pprint(s)
#
#l = Lease()
#l.slice_id = s.id
#l.start_time = 1458640800
#l.duration = 3600
##l.end_time = 1458324000
## XXX In builder check that resources belong to the right testbed
#l.addResources(r)
#pprint(l)
#
#s.addLease(l)
#
#pprint(s)
#s = s.save()
#pprint(s)

# print(time.time()-start_time)
# auths = q(Authority).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
# for auth in auths:
#     print(auth.id)

proj = q(Project).id('urn:publicid:IDN+onelab:upmc:infocom+authority+sa').get()
#for p in proj:
#    print('Project')
#    pprint(p.attributes())
#
#proj = q(Project).get()
#for p in proj:
#    print(p.id)
#
pprint(proj)

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

