'''
Base API Class

'''
from myslicelib.util.url import validateUrl

class Endpoint(object):
    """
    An endpoint specifies a remote API endpoint.
    type is the type of endpoint, e.g. AM, Reg
    protocol specifies the protocol, default is SFA
    url is the remote url
    """

    def __init__(self, type="AM", protocol="SFA", url=None):
        self.type = type
        self.protocol = protocol
        if not url or not validateUrl(url):
            raise ValueError("URL not valid")
        else:
            self.url = url



    def __str__(self):
        return self.url


class Api(object):
    """
    This is the generic "facade" API interface to the actual API interfaces to the AM and Registry endpoints
    Depending on the protocol a different AM and Registry API is needed, e.g. SFA needs two separate endpoints,
    MyPLC only one.

    This class will instantiate two classes, one am and one reg, if the protocol provides only one endpoint
    it will be used for both functions (am and reg).

    AM class will manage:
    - Resources list
    - Slice resource provisioning (with and without lease)

    Registry class will manage:
    - Slice creation, update, delete
    - Authority creation, update, delete
    - User creation, update, delete

    """

    def __init__(self, endpoints: Endpoint) -> None:
        self.endpoints = []
        for endpoint in endpoints:
            self.endpoints.append

    def version(self) -> dict:
        result = { "MySlice Lib API" : { "version" : "1.0" } }
        for e in self.endpoints:
            result[e.type + " API"] = {
                "type" : e.type,
                "protocol" : e.protocol,
                "url" : e.url
            }
        return result

    def get(self):
        raise NotImplementedError('Not implemented')

    def update(self):
        raise NotImplementedError('Not implemented')

    def delete(self):
        raise NotImplementedError('Not implemented')