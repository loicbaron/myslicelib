import os

from myslicelib import setup as s
from myslicelib.util import Endpoint, Credential

s.endpoints = [
    #Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
    #Endpoint(url="https://194.199.16.164:12346",type="AM"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    #Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]


if os.path.exists("/root/.sfi/"):
    path = "/root/.sfi/"
    pkey = path + "onelab.upmc.loic_baron.pkey"
    hrn = "onelab.upmc.loic_baron"
    email = "loic.baron@lip6.fr"
    cert = path + "onelab.upmc.loic_baron.user.gid"
else:
    path = "/root/"
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

s.credential = Credential(hrn=hrn, email=email, certificate=cert, private_key=pkey)
