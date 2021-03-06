'''
Base API Class

'''
import threading
from queue import Queue
from myslicelib.util import Endpoint, Authentication
from myslicelib.api.sfaam import SfaAm
from myslicelib.api.sfareg import SfaReg
#from myslicelib.util.certificate import Keypair, Certificate
import concurrent.futures

from pprint import pprint

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

    def __init__(self, endpoints: Endpoint, authentication: Authentication) -> None:
        if not isinstance(endpoints, list) or not all(isinstance(endpoint, Endpoint) for endpoint in endpoints):
            raise ValueError("API needs an object of type Endpoint, please check the configuration")

        if not isinstance(authentication, Authentication):
            raise ValueError("API needs Authentication, please check your private key or generate a new one")

        self.registry = None # at least one registry endpoint must be present
        self.ams = [] # one or plus am must be present, this depends on the am to be present

        # search for the registry
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "Reg"):
                self.registry = SfaReg(endpoint, authentication)
                registry_endpoint = endpoint
                break

        if not self.registry:
            raise ValueError("At least a Registry must be specified")

        # search for the AMs
        for endpoint in endpoints:
            if (endpoint.protocol == "SFA") and (endpoint.type == "AM"):
                self.ams.append( SfaAm(endpoint,  SfaReg(registry_endpoint, authentication)) )

    def __getattr__(self, entity):
        def method_handler():
            if not entity in self._entities:
                raise NotImplementedError("Invalid object {} or not implemented".format(entity))

            self._entity = entity
            return self

        return method_handler

    def _thread_handler(self, call, *params):
        return {call: params}

    def _parallel_request(self, threads):
        result = {'data':[],'errors':[]}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for thread in threads:
                for call, arg in thread.items():
                    if arg:
                        future = executor.submit(call, *arg)
                    else:
                        future = executor.submit(call)
                    res = future.result()
                    #try:
                    #    res = future.result(timeout=5)
                    #except concurrent.futures.TimeoutError as e:
                    #    res = {'data':[],'errors':[e]}
                    result['data'] += res['data']
                    result['errors'] += res['errors']
        return result


    def version(self):
        threads= [self._thread_handler(self.registry.version)] + \
                 [self._thread_handler(am.version) for am in self.ams]

        res = self._parallel_request(threads)
        #pprint(res)
        return res

    def get_credentials(self, ids, delegated_to=None):
        result = {}
        threads = []
        for id in ids:
            threads += [self._thread_handler(self.registry.get_credential,id,delegated_to)]
        result = self._parallel_request(threads)
        return result

    def get(self, id=None, raw=False):
        result = {}
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

    def update(self, id, params):
        if not isinstance(params, dict):
            raise MysParamsTypeError('a dict is expected')
        
        result = {}
        threads = []
        if self._entity in self._registry:
            res_get = self.registry.get(self._entity, id)
            if len(res_get['errors']) > 0 or len(res_get['data']) == 0:
                # Re-Initialize the logs
                self.registry.logs = []
                res_reg = self.registry.create(self._entity, id, params)
            else:
                res_reg = self.registry.update(self._entity, id, params)
            # XXX We should flag if Exception is raised
            # XXX because for Slice if Registry call failed we will not call the AMs

        if self._entity in self._am:
            for am in self.ams:
                threads += [self._thread_handler(am.update, self._entity, id, params)]

        res_am = self._parallel_request(threads)
        result['data'] = res_reg['data']
        result['errors'] = res_reg['errors']
        if res_am['data']:
            result['data'] += merge_dicts(res_am['data'])
        if res_am['errors']:
            result['errors'] += res_am['errors']

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


def merge_dicts(res):
    result = {}
    # element could be slice from reg
    # could be resources from am, leases from am
    for element in res:
        if isinstance(element, dict):
            for key, value in element.items():
                if key in result:
                    # append
                    result[key] += value
                else:
                    result[key] = value
        else:
            result = res
    return [result]
