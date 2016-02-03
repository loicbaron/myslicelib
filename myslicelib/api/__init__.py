'''
Base API Class

'''
from myslicelib.util import Endpoint, Credential
from myslicelib.api.sfaam import SfaAm
from myslicelib.api.sfareg import SfaReg
#from myslicelib.util.certificate import Keypair, Certificate

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

    def __init__(self, endpoints: Endpoint, credential: Credential) -> None:
        self.endpoints = []
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "AM"):
                self.endpoints.append( SfaAm(endpoint, credential) )
            elif (endpoint.protocol == "SFA") and (endpoint.type == "Reg"):
                self.endpoints.append( SfaReg(endpoint, credential) )
            else:
                raise ValueError

    def version(self) -> dict:
        result = { "MySlice Lib API" : { "version" : "1.0" } }
        for e in self.endpoints:
            result[e.endpoint.type + " API"] = {
                "type" : e.endpoint.type,
                "protocol" : e.endpoint.protocol,
                "url" : e.endpoint.url
            }
        return result

    def get(self):
        raise NotImplementedError('Not implemented')

    def update(self):
        raise NotImplementedError('Not implemented')

    def delete(self):
        raise NotImplementedError('Not implemented')