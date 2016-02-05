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
        self.registry = None # at least one registry endpoint must be present
        self.ams = [] # one or plus am must be present, this depends on the am to be present

        # search for the registry
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "Reg"):
                self.registry = SfaReg(endpoint, credential)
                break

        if not self.registry:
            raise ValueError("At least a Registry must be specified")

        # search for the AMs
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "AM"):
                self.ams.append( SfaAm(endpoint, self.registry) )

    def version(self) -> dict:
        result = {
                "MySlice Lib API" : {
                    "version" : "1.0"
                },
                "Registry" : {
                    "protocol" : self.registry.endpoint.protocol,
                    "url" : self.registry.endpoint.url,
                    "version" : self.registry.version()
                }
            }
        # for e in self.endpoints:
        #     result[e.endpoint.type + " API"] = {
        #         "type" : e.endpoint.type,
        #         "protocol" : e.endpoint.protocol,
        #         "url" : e.endpoint.url,
        #         "protocol_version" : e.version()['version']
        #     }
        return result

    def get(self):
        raise NotImplementedError('Not implemented')

    def update(self, type, object, id, endpoint):
        raise NotImplementedError('Not implemented')

    def delete(self):
        raise NotImplementedError('Not implemented')