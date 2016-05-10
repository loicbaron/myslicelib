import os

from myslicelib import setup as s
from myslicelib.util import Endpoint, Authentication

s.endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM", name="PLE", timeout=30),
    #Endpoint(url="https://194.199.16.164:12346",type="AM"),
    #Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
    #Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
    #Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg", name="OneLab Reg", timeout=10),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]


if os.path.exists(os.path.expanduser("~/.sfi/")):
    path = os.path.expanduser("~/.sfi/")
    pkey = path + "onelab.upmc.loic_baron.pkey"
    hrn = "onelab.upmc.loic_baron"
    email = "loic.baron@lip6.fr"
    cert = path + "onelab.upmc.loic_baron.user.gid"

#if os.path.exists("/root/.sfi"):
#    path = "/root/.sfi/"
#    pkey = path + "onelab.upmc.joshzhou16.pkey"
#    cert = path + "onelab.upmc.joshzhou16.sscert"
#    hrn = "onelab.upmc.joshzhou16"
#    email = "joshzhou16@gmail.com"
else:
    path = os.path.expanduser("~/")
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
