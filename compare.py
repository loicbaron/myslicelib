#!/usr/bin/env python3.5
import asyncio
import time

from myslicelib.util import Endpoint, Authentication
from myslicelib.api import Api
from myslicelib.api.aioapi import Aioapi

path = "/var/myslice/"
pkey = path + "myslice.pkey"
hrn = "onelab.myslice"
email = "support@myslice.info"
cert = path + "myslice.cert"

authentication = Authentication(hrn=hrn, email=email,
                                certificate=cert, private_key=pkey)

endpoints = [
    Endpoint(url="https://sfa3.planet-lab.eu:12346", type="AM", name="PLE", timeout=30),
    Endpoint(url="https://194.199.16.164:12346", type="AM"),
    Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0", type="AM"),
    Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2", type="AM"),
    Endpoint(url="https://portal.onelab.eu:6080", type="Reg", name="OneLab Reg", timeout=10),
]


def timeit(method=None):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time() - start_time
        print(end_time) 
        return result
    return timed

@timeit
def async_api(loop):
    instance = Aioapi(endpoints=endpoints,
                   authentication=authentication,
                   loop=loop)

    result = instance.version()
    return result 

@timeit
def sync_api():
    instance = Api(endpoints=endpoints,
                   authentication=authentication)
    return instance.version()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(async_api(loop))
    print(sync_api())
    print(async_api(loop))
    loop.close()



