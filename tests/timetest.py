import time 
import logging
from collections import OrderedDict
import multiprocessing

from myslicelib.api import Api 
from myslicelib.api.sfareg import SfaReg
from myslicelib.api.sfaam import SfaAm
from myslicelib.util import Endpoint, Authentication
from myslicelib import setup as s

from config import loic, quan
from singleton import Singleton

request_rspec = OrderedDict([(u'rspec', OrderedDict([(u'@xmlns:xsi', u'http://www.w3.org/2001/XMLSchema-instance'), (u'@xmlns', u'http://www.geni.net/resources/rspec/3'), (u'@xmlns:plos', u'http://www.planet-lab.org/resources/sfa/ext/plos/1'), (u'@xmlns:planetlab', u'http://www.planet-lab.org/resources/sfa/ext/planetlab/1'), (u'@type', u'request'), (u'@xsi:schemaLocation', u'http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://www.planet-lab.org/resources/sfa/ext/planetlab/1 http://www.planet-lab.org/resources/sfa/ext/planetlab/1/planetlab.xsd http://www.planet-lab.org/resources/sfa/ext/plos/1 http://www.planet-lab.org/resources/sfa/ext/plos/1/plos.xsd'), (u'@expires', u'2016-05-30T17:07:46Z'), (u'@generated', u'2014-05-30T16:07:46Z'), (u'node', [OrderedDict([(u'@component_manager_id', u'urn:publicid:IDN+ple+authority+cm'), (u'@component_id', u'urn:publicid:IDN+ple:uitple+node+planetlab1.cs.uit.no'), (u'@exclusive', u'false'), (u'@component_name', u'planetlab1.cs.uit.no'), (u'sliver_type', OrderedDict([(u'@name', u'plab-vserver')]))]), OrderedDict([(u'@component_manager_id', u'urn:publicid:IDN+ple+authority+cm'), (u'@component_id', u'urn:publicid:IDN+ple:unioslople+node+planetlab2.ifi.uio.no'), (u'@exclusive', u'false'), (u'@component_name', u'planetlab2.ifi.uio.no'), (u'sliver_type', OrderedDict([(u'@name', u'plab-vserver')]))])])]))])

def timeit(loops=10):
    def measuretime(method):
        def timed(*args, **kw):
            sums = 0.0
            mins = 1.7976931348623157e+308
            maxs = 0.0
            for i in range(0, loops):
                t0 = time.time()
                result = method(*args,**kw)
                dt = time.time() - t0
                mins = dt if dt < mins else mins
                maxs = dt if dt > maxs else maxs
                sums += dt
            
            #logging.info('%r min run time was %2.9f sec' % (method.__name__,mins))
            #logging.info('%r max run time was %2.9f sec' % (method.__name__,maxs))
            logging.info('%r avg run time was %2.9f sec in %s runs' % (method.__name__,sums/loops,loops))
            return result
        return timed
    return measuretime

def log(func):   
    def wrapper(*args, **kwargs):
        root = 'logs/' + func.__name__.split('_')[0] + '/'
        logging.basicConfig(filename=root+func.__name__+'.log', 
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p'
                            )
        return func(*args, **kwargs)
    return wrapper

class MeasureSfaApi(Singleton):

    _loops = 1

    def setup(self, config):
        s.endpoints = [
                Endpoint(url=config['url_am'], type ='AM'),
                Endpoint(url=config['url_registry'], type = 'Reg')
            ]
        s.authentication = Authentication(  email=config['email'], 
                                    hrn=config['hrn'], 
                                    private_key=config['pkey'], 
                                    certificate=config['cert'])
        self.api = Api(s.endpoints, s.authentication)
        return self

    @timeit(loops=_loops) 
    def measure_registry_get_authority_credential(self):
        print(self.api.registry.get_credential('onelab.upmc.apitest', 'authority'))

    @timeit(loops=_loops) 
    def measure_registry_get_slice_credential(self):
        self.api.registry.get_credential('onelab.upmc.apitest.slice', 'slice')

    @timeit(loops=_loops) 
    def measure_registry_get_user(self):
        self.api.registry.get('onelab.upmc.apitest.aaaa')

    @timeit(loops=_loops) 
    def measure_registry_get_authority(self):
        self.api.registry.get('onelab.upmc.apitest')

    @timeit(loops=_loops)
    def measure_registry_get_slice(self):
        self.api.registry.get('onelab.upmc.apitest.slicey')

    @timeit(loops=_loops)
    def measure_registry_list_authoiry(self):
        self.api.registry.get(hrn='onelab.upmc.apitest.', list=True)

    @timeit(loops=_loops)
    def measure_registry_list_all(self):
        self.api.registry.get()

    # @timeit(loops=_loops)
    # def measure_registry_create_user(self):
    #     record_dict = { 
    #                     'hrn': 'onelab.upmc.apitest.foo',
    #                     'email': 'bbbb_old@onelab.eu',
    #                     'reg-keys': ['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAA\
    #                                   AAgQD3iRxbPseM1ZIvuZUrQ1p/4KKCqD38\
    #                                   b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QK\
    #                                   n17ddZ2mnWN1YZuFlSaiD64rpQT6guoGSj\
    #                                   XtQmHqq97lH037/LphRYs2BY6ZknlLGvTP\
    #                                   cP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ==']
    #                     }
    #     self.api.registry.create(record_dict, 'user')

    # @timeit()
    # def measure_registry_create_slice(self):
    #     record_dict = {
    #                     'hrn': 'onelab.upmc.apitest.slicex',
    #                     'reg-researchers':['onelab.upmc.apitest.aaaa']
    #                     }
    #     self.api.registry.create(record_dict, 'slice')

    # @timeit()
    # def meausure_registry_create_authority(self):
    #     record_dict = {
    #                     'hrn':'onelab.upmc.apitest.auth', 
    #                     'reg-pis':['onelab.upmc.apitest.aaaa']
    #                     }
    #     self.api.registry.create(record_dict, 'authority')

    # @timeit()
    # def measure_registry_update_user(self):
    #     record_dict = { 
    #                     'hrn': 'onelab.upmc.apitest.foo',
    #                     'email': 'foo_new@onelab.eu',
    #                     'reg-keys': ['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAA\
    #                                   AAgQD3iRxbPseM1ZIvuZUrQ1p/4KKCqD38\
    #                                   b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QK\
    #                                   n17ddZ2mnWN1YZuFlSaiD64rpQT6guoGSj\
    #                                   XtQmHqq97lH037/LphRYs2BY6ZknlLGvTP\
    #                                   cP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ==']
    #                     }
    #     self.api.registry.create(record_dict, 'user')

    # @timeit()
    # def measure_registry_update_slice(self):
    #     record_dict = {
    #                     'hrn': 'onelab.upmc.apitest.slicefoo',
    #                     'reg-researchers':['onelab.upmc.apitest.aaaa']
    #                     }
    #     self.api.registry.create(record_dict, 'slice')

    # @timeit()
    # def measure_registry_update_authority(self):
    #     record_dict = {
    #                     'hrn':'onelab.upmc.apitest.auth', 
    #                     'reg-pis':['onelab.upmc.apitest.aaaa']
    #                     }
    #     self.api.registry.create(record_dict, 'authority')

    # @timeit()
    # def measure_registry_delete_user(self):
    #     self.api.registry.delete('onelab.upmc.apitest.foo', 'user')

    # @timeit()
    # def measure_registry_delete_slice(self):
    #     self.api.registry.delete('onelab.upmc.apitest.slicefoo', 'slice')

    # @timeit()
    # def measure_registry_delete_authority(self):
    #     self.api.registry.delete('onelab.upmc.apitest.auth', 'authority')

    # @timeit(loops=10)
    # def measure_ams_list_resource(self):
    #     logging.info('test with %i AM' % len(self.api.ams))
    #     for am in self.api.ams:
    #         am.list('resource')

    # @timeit()
    # def measure_ams_list_lease(self):
    #     logging.info('test with %i AM' % len(self.api.ams))
    #     for am in self.api.ams:
    #         am.list('lease')

    # @timeit()
    # def measure_ams_create_slice(self):
    #     record_dict = {
    #                     'hrn': 'onelab.upmc.apitest.foo',
    #                     'parsed': request_rspec, 
    #                     }
    #     logging.info('test with %i AM' % len(self.api.ams))
    #     for am in self.api.ams:
    #         am.create(record_dict, 'slice')


    # @timeit()
    # def measure_ams_update_slice(self):
    #     record_dict = {
    #                     'hrn': 'onelab.upmc.apitest.slicefoo',
    #                     'parsed': request_rspec, 
    #                     }
    #     logging.info('test with %i AM' % len(self.api.ams))
    #     for am in self.api.ams:
    #         am.create(record_dict, 'slice')

    # @timeit()
    # def measure_ams_delete_slice(self):
    #     logging.info('test with %i AM' % len(self.api.ams))
    #     for am in self.apit.ams:
    #         am.create('onelab.upmc.apitest.slicefoo')


class Logs(object):
    
    def __init__(self, measure_obj):
        self.m = measure_obj

    @log 
    def get(self):
        self.m.measure_registry_get_user()
        self.m.measure_registry_get_slice()
        self.m.measure_registry_get_authority()
        self.m.measure_registry_list_all()
        self.m.measure_registry_list_authoiry()

def worker():
    m = MeasureSfaApi().setup(quan)
    l = Logs(m)
    l.get()

if __name__ == '__main__':
    wnumber = 30
    logging.info('======concurrent worker is %s ==========' % wnumber)
    for i in range(wnumber):
        p = multiprocessing.Process(target=worker)
        p.start()
