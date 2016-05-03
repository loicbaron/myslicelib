#!/usr/bin/env python3.5
import sys
from myslicelib.util import Endpoint, Credential
from myslicelib.api import Api

from myslicelib import setup as s
from myslicelib.model.testbed import Testbed
from myslicelib.model.user import User
from myslicelib.model.slice import Slice
from myslicelib.query import q

import subprocess

s.endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM",name="PlanetLab Europe"),
    Endpoint(url="https://194.199.16.164:12346",type="AM",name="IoTLab"),
    Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM",name="WiLab.t"),
    Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM",name="FUSECO"),
    Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM",name="NITOS Paris"),
    Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
    #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
]

path = "/Users/moray/Sites/upmc/"
pkey = path + "cscognamiglio_onelab.pkey"
hrn = "onelab.upmc.cscognamiglio"
email = "cscognamiglio@gmail.com"
cert = path + "cscognamiglio_onelab.cert"

s.authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)


class TestbedNew(Testbed):

    def ping(self):
        ping = subprocess.Popen(
                ["ping", "-c", "1", self.ip],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
                )
        out, err = ping.communicate()
        return ping.returncode


# testbeds = q(TestbedNew).get()
#
# for t in testbeds:
#     print(t.name, t.hostname, t.ip, t.api, type(t))

users = q(User).id("onelab.upmc.cscognamiglio").get()
for u in users:
    print("{} - {}".format(u.email, type(u)))

#
# slices = q(Slice).id('onelab').get()
# for s in slices:
#     print("{} - {}".format(s.name, type(s)))
