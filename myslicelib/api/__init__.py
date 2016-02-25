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

    _entities = [
        'resource',
        'slice',
        'user',
        'authority'
    ]

    _am = [
        'resource'
    ]

    _registry = [

    ]

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

    def __getattr__(self, entity):

        def methodHandler():
            if not entity in self._entities:
                raise NotImplementedError("Invalid object {} or not implemented".format(entity))

            self._entity = entity

            return self

        return methodHandler


    def version(self) -> dict:
        result = {
                "myslicelib" : {
                    "version" : "1.0"
                },
                "registry" : {
                    "type" : "registry",
                    "protocol" : self.registry.endpoint.protocol,
                    "url" : self.registry.endpoint.url,
                    "version" : self.registry.version()
                },
                "ams" : []
            }

        for am in self.ams:
            result["ams"].append( {
                "type" : am.endpoint.type,
                "protocol" : am.endpoint.protocol,
                "url" : am.endpoint.url,
                "version" : am.version()
            } )

        return result


    def get(self, id=None):
        result = []
        if self._entity in self._am:
            for am in self.ams:
                result.append(
                    am.get(self._entity)
                )

        return result

        # if (id) :
        #     return self.registry.get(hrn=id, object_type=self.object_type)
        # else :
        #     return self.registry.list(object_type=self.object_type)
        #
        # raise NotImplementedError('Not implemented')

    def update(self, type, object, id, endpoint):
        raise NotImplementedError('Not implemented')

    def delete(self):
        raise NotImplementedError('Not implemented')