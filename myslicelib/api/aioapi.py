import asyncio

from myslicelib.util import Endpoint, Authentication
from myslicelib import setup as s
from myslicelib.api.aiosfa import Sfa
from concurrent.futures import ProcessPoolExecutor

class Aioapi(object):
    """
    This is the generic "facade" API interface to the actual API interfaces
    to the AM and Registry endpoints.
    Depending on the protocol a different AM and Registry API is needed,
    e.g. SFA needs two separate endpoints, MyPLC only one.

    This class will instantiate two classes, one am and one reg,
    if the protocol provides only one endpoint
    it will be used for both functions (am and reg).

    AM class will manage:
    - Resources list
    - Slice resource provisioning (with and without lease)

    Registry class will manage:
    - Slice creation, update, delete
    - Authority creation, update, delete
    - User creation, update, delete

    """
    _entities = [
        'testbed',
        'resource',
        'slice',
        'user',
        'authority',
        'lease',
        'project'
    ]

    _am = [
        'resource',
        'slice',
        'lease'
    ]

    _registry = [
        'slice',
        'user',
        'authority',
        'project'
    ]

    def __init__(self, endpoints: Endpoint, authentication: Authentication, loop=None) -> None:
        if (not isinstance(endpoints, list) or
            not all(isinstance(endpoint, Endpoint) for endpoint in endpoints)):
            raise ValueError("API needs an object of type Endpoint")

        if not isinstance(authentication, Authentication):
            raise ValueError("API needs an object of type Authentication")

        # at least one registry endpoint must be present
        self.registry = None
        self.ams = []

        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "Reg"):
                self.registry = Sfa(endpoint, authentication)
                # self.registry = SfaReg(endpoint, authentication)
                registry_endpoint = endpoint
                break

        if not self.registry:
            raise ValueError("At least a Registry must be specified")

        # search for the AMs
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "AM"):
                self.ams.append(Sfa(endpoint, authentication))
                # self.ams.append(SfaAm(endpoint,
                #                     SfaReg(registry_endpoint, authentication)))

        self.agents = self.ams + list(registry)

        self._loop = loop or asyncio.get_event_loop()

    def _async_tasks(self, agents, method, *args):
        if args:
            tasks = [
                asyncio.ensure_future(
                        getattr(agent, method)(args)
                    ) for agent in agents
                ]
        else:
            tasks = [
                asyncio.ensure_future(
                        getattr(agent, method)()
                    ) for agent in agents
                ]
        result = self._loop.run_until_complete(asyncio.gather(*tasks))
        return result

    def version(self):
        return self._async_tasks(self.agents, method='version')

    def get(self):
        return self._async_tasks(self.agents, method='get')

    def update(self):
        return self._async_tasks(self.agents, method='update')

    def delete(self):
        return self._async_tasks(self.agents, method='delete')






if __name__ == '__main__':

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

    loop = asyncio.get_event_loop()
    import time
    start = time.clock()
    instance = Aioapi(endpoints=endpoints,
                      authentication=authentication,
                      loop=loop)

    instance.version()
    end = time.clock()
    print(end - start)


    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(instance.version())
    # loop.stop()
