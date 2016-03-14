'''
Base API Class

'''
import threading
from queue import Queue
from urllib.parse import urlparse
from myslicelib.util import Endpoint, Credential
from myslicelib.api.sfaam import SfaAm
from myslicelib.api.sfareg import SfaReg
#from myslicelib.util.certificate import Keypair, Certificate
import concurrent.futures


from myslicelib.error import MysParamsTypeError

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

    _q = Queue()

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
                registry_endpoint = endpoint
                break

        if not self.registry:
            raise ValueError("At least a Registry must be specified")

        # search for the AMs
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "AM"):
                self.ams.append( SfaAm(endpoint,  SfaReg(registry_endpoint, credential)) )


    def __getattr__(self, entity):

        def method_handler():
            if not entity in self._entities:
                raise NotImplementedError("Invalid object {} or not implemented".format(entity))

            self._entity = entity

            return self

        return method_handler

    def _queue_hanlder(self, call, *params):
        if params is None:
            self._q.put(call())
        else:
            self._q.put(call(*params))

    def _thread_handler(self, call, *params):
        return threading.Thread(target=self._queue_hanlder, args=(call, *params))

    def _parallel_request(self, threads):
        result = []
        with self._q.mutex:
            self._q.queue.clear() 
        try:
            for t in threads:
                t.start()
            for t in threads:
                t.join()        
            for _ in threads:            
                res = self._q.get(block=False)
                if isinstance(res, list):
                    result += res
                else:
                    result += [res]
            return result
        except Exception as e:
            print(e)
            return result


    # def _thread_handler(self, call, *params):
    #     return {call: params}

    # @time.timeit
    # def _parallel_request(self, threads):
    #     result = []
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         for thread in threads:
    #             for call, arg in thread.items():
    #                 if arg:
    #                     future = executor.submit(call, *arg)
    #                 else:
    #                     future = executor.submit(call)
    #                 result += [future.result()]
    #     return result


    def version(self):
        threads= [self._thread_handler(self.registry.version)] + \
                 [self._thread_handler(am.version) for am in self.ams]

        res = self._parallel_request(threads)

        reg_version = res[0]
        del res[0]

        result = {
                "myslicelib" : {
                    "version" : "1.0"
                },
                "registry" : {
                    "url" : self.registry.endpoint.url,
                    "hostname" : urlparse(self.registry.endpoint.url).hostname,
                    "name" : self.registry.endpoint.name,
                    "status" : reg_version['status'],
                    "api" : {
                        "type" : "registry",
                        "protocol" : self.registry.endpoint.protocol,
                        "version" : reg_version['version'],
                    },
                    "id" : reg_version['id'],
                },
                "ams" : []
            }

        for i, am in enumerate(self.ams):
            result["ams"].append( {
                "url" : am.endpoint.url,
                "hostname" : urlparse(am.endpoint.url).hostname,
                "name" : am.endpoint.name,
                "status" : res[i]['status'],
                "api" : {
                    "type" : am.endpoint.type,
                    "protocol" : am.endpoint.protocol,
                    "version" : res[i]['version'],
                },
                "id" : res[i]['id'],
            } )

        return result

    def get(self, id=None, raw=False):
        result = []
        threads = []
        
        if self._entity in self._am:
            for am in self.ams:
                threads += [self._thread_handler(am.get, self._entity, id, raw)]

        if self._entity in self._registry:
            threads += [self._thread_handler(self.registry.get, self._entity, id)]

        if self._entity not in self._am and self._entity not in self._registry:
            raise NotImplementedError('Not implemented')


        result = self._parallel_request(threads)
        return result

        # if (id) :
        #     return self.registry.get(hrn=id, object_type=self.object_type)
        # else :
        #     return self.registry.list(object_type=self.object_type)
        #
        # raise NotImplementedError('Not implemented')

    def update(self, id, params):
        if not isinstance(params, dict):
            raise MysParamsTypeError('a dict is expected')
        
        result = []
        threads = []
        if self._entity in self._registry:
            result += self.registry.create(self._entity, id, params)
            if not result:
                result += self.registry.update(self._entity, id, params)

        if self._entity in self._am:
            for am in self.ams:
                threads += [self._thread_handler(am.update, self._entity, id, params)]

        result += self._parallel_request(threads)

        # if self._entity in self._registry:
        #     result += self.registry.create(self._entity, id, params)
        #     if not result:
        #         result += self.registry.update(self._entity, id, params)

        # if self._entity in self._am:
        #     for am in self.ams:
        #         result += am.update(self._entity, id, params)

        if self._entity not in self._am and self._entity not in self._registry:
            raise NotImplementedError('Not implemented')

        return result


    def delete(self, id):
        exists = self.get(id)
        threads = []
        result = True
        if not exists:
            raise Exception('This object do not exist')
        else:
            if self._entity in self._am:
                for am in self.ams:
                    threads += [self._thread_handler(am.delete, self._entity, id)]
            
            if self._entity in self._registry:
                threads += [self._thread_handler(self.registry.delete, self._entity, id)]

            result = self._parallel_request(threads)

            if self._entity not in self._am and self._entity not in self._registry:
                raise NotImplementedError('Not implemented')

        return result
