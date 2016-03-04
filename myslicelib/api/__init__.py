'''
Base API Class

'''
from urllib.parse import urlparse
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
        'testbed',
        'resource',
        'slice',
        'user',
        'authority',
        'lease'
    ]

    _am = [
        'resource',
        'slice',
        'lease'
    ]

    _registry = [
        'slice',
        'user',
        'authority'
    ]

    def __init__(self, endpoints: Endpoint, credential: Credential) -> None:

        if not isinstance(endpoints, list) or not all(isinstance(endpoint, Endpoint) for endpoint in endpoints):
            raise ValueError("API needs an object of type Endpoint")

        if not isinstance(credential, Credential):
            raise ValueError("API needs an object of type Credential")

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

        def method_handler():
            if not entity in self._entities:
                raise NotImplementedError("Invalid object {} or not implemented".format(entity))

            self._entity = entity

            return self

        return method_handler


    def version(self) -> dict:
        result = {
                "myslicelib" : {
                    "version" : "1.0"
                },
                "registry" : {
                    "url" : self.registry.endpoint.url,
                    "hostname" : urlparse(self.registry.endpoint.url).hostname,
                    "name" : self.registry.endpoint.name,
                    "status" : self.registry.version()['status'],
                    "api" : {
                        "type" : "registry",
                        "protocol" : self.registry.endpoint.protocol,
                        "version" : self.registry.version()['version'],
                    },
                    "id" : self.registry.version()['id'],
                },
                "ams" : []
            }

        for am in self.ams:
            result["ams"].append( {
                "url" : am.endpoint.url,
                "hostname" : urlparse(am.endpoint.url).hostname,
                "name" : am.endpoint.name,
                "status" : am.version()['status'],
                "api" : {
                    "type" : am.endpoint.type,
                    "protocol" : am.endpoint.protocol,
                    "version" : am.version()['version'],
                },
                "id" : am.version()['id'],
            } )

        return result


    def get(self, id=None, raw=False):
        result = []
        if self._entity in self._registry:
            result += self.registry.get(self._entity, id)

        if self._entity in self._am:
            for am in self.ams:
                result += am.get(self._entity, id, raw)
        
        if self._entity not in self._am and self._entity not in self._registry:
            raise NotImplementedError('Not implemented')

        return result

        # if (id) :
        #     return self.registry.get(hrn=id, object_type=self.object_type)
        # else :
        #     return self.registry.list(object_type=self.object_type)
        #
        # raise NotImplementedError('Not implemented')

    def update(self, id, params):
        result = []
        if self._entity in self._registry:
            result += self.registry.create(self._entity, id, params)
            if not result:
                result += self.registry.update(self._entity, id, params)

        if self._entity in self._am:
            for am in self.ams:
                result += am.update(self._entity, id, params)

        if self._entity not in self._am and self._entity not in self._registry:
            raise NotImplementedError('Not implemented')

        return result


    def delete(self, id):
        exists = self.get(id)
        if not exists:
            raise Exception('This object do not exist')
        else:
            if self._entity in self._am:
                for am in self.ams:
                    result = am.delete(self._entity, id)
            if self._entity in self._registry:
                result = self.registry.delete(self._entity, id)

            if self._entity not in self._am and self._entity not in self._registry:
                raise NotImplementedError('Not implemented')

        return result
