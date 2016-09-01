#!/usr/bin/env python3.5
import asyncio
import time

from myslicelib.util import Endpoint, Authentication
from myslicelib.api import Api
from myslicelib.api.aioapi import Aioapi

from myslicelib.api.sfareg import SfaReg
from myslicelib.api.aiosfareg import AiosfaReg

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

# @timeit
# def async_reg(loop):
#     endpoint = Endpoint(url="https://portal.onelab.eu:6080", type="Reg", name="OneLab Reg", timeout=10)
#     authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)
#     instance = AiosfaReg(endpoint, authentication)
#     get = asyncio.gather(instance.get('project'), return_exceptions=True)
#     loop.run_until_complete(get)
#     return get.result()

@timeit
def async_reg(loop):
    endpoint = Endpoint(url="https://portal.onelab.eu:6080", type="Reg", name="OneLab Reg", timeout=10)
    authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)
    instance = AiosfaReg(endpoint, authentication)
    get = asyncio.gather(instance.get('slice', urn='urn:publicid:IDN+onelab:asdas:yasintest+slice+sliceyasin'), return_exceptions=True)
    loop.run_until_complete(get)
    return get.result()

@timeit
def sync_reg():
    endpoint = Endpoint(url="https://portal.onelab.eu:6080", type="Reg", name="OneLab Reg", timeout=10)
    authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)
    instance = SfaReg(endpoint, authentication)
    return instance.get('slice', urn='urn:publicid:IDN+onelab:asdas:yasintest+slice+sliceyasin')

if __name__ == '__main__':
    from pprint import pprint
    loop = asyncio.get_event_loop()
    # print(async_api(loop))
    # print(sync_api())
    # print(async_api(loop))
    # loop.close()

    #pprint(sync_reg())
    pprint(async_reg(loop))
    #async_reg(loop)





