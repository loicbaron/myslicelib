#!/bin/env python3

'''
DISCLAIMER: this is a file to test during development, needs to be removed
'''
import datetime
import xmltodict
from myslicelib.api.sfareg import SfaReg
from myslicelib.api.sfaam import SfaAm
from myslicelib.util import Endpoint, Credential
from pprint import pprint
from collections import OrderedDict


request_rspec = OrderedDict([(u'rspec', OrderedDict([(u'@xmlns:xsi', u'http://www.w3.org/2001/XMLSchema-instance'), (u'@xmlns', u'http://www.geni.net/resources/rspec/3'), (u'@xmlns:plos', u'http://www.planet-lab.org/resources/sfa/ext/plos/1'), (u'@xmlns:planetlab', u'http://www.planet-lab.org/resources/sfa/ext/planetlab/1'), (u'@type', u'request'), (u'@xsi:schemaLocation', u'http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://www.planet-lab.org/resources/sfa/ext/planetlab/1 http://www.planet-lab.org/resources/sfa/ext/planetlab/1/planetlab.xsd http://www.planet-lab.org/resources/sfa/ext/plos/1 http://www.planet-lab.org/resources/sfa/ext/plos/1/plos.xsd'), (u'@expires', u'2016-05-30T17:07:46Z'), (u'@generated', u'2014-05-30T16:07:46Z'), (u'node', [OrderedDict([(u'@component_manager_id', u'urn:publicid:IDN+ple+authority+cm'), (u'@component_id', u'urn:publicid:IDN+ple:uitple+node+planetlab1.cs.uit.no'), (u'@exclusive', u'false'), (u'@component_name', u'planetlab1.cs.uit.no'), (u'sliver_type', OrderedDict([(u'@name', u'plab-vserver')]))]), OrderedDict([(u'@component_manager_id', u'urn:publicid:IDN+ple+authority+cm'), (u'@component_id', u'urn:publicid:IDN+ple:unioslople+node+planetlab2.ifi.uio.no'), (u'@exclusive', u'false'), (u'@component_name', u'planetlab2.ifi.uio.no'), (u'sliver_type', OrderedDict([(u'@name', u'plab-vserver')]))])])]))])

def test_by_loic():
    path = "/root/.sfi/"
    pkey = path + "onelab.upmc.loic_baron.pkey"
    cert = path + "onelab.upmc.loic_baron.sscert"
    
    hrn = "onelab.upmc.loic_baron"
    email = "loic.baron@lip6.fr"
    url_am = "https://sfa3.planet-lab.eu:12346" 
    url_registry = "https://portal.onelab.eu:6080"
    #url_registry = "http://dev.myslice.info:12345"

    endpoint_registry = Endpoint(url=url_registry)
    endpoint_am = Endpoint(url=url_am)
    credential = Credential(email=email, hrn=hrn, private_key=pkey, certificate=cert)
    Registry = SfaReg(endpoint_registry, credential)
    AM = SfaAm(endpoint_am, Registry)

    #print(Registry.version())
    #print(Registry.get(hrn))
    #pprint(Registry.list())
    #pprint(Registry.list("onelab.upmc"))

    print("=====user test=======")
    user_dict = {'hrn':'onelab.upmc.aaaa','email':'aaaa@onelab.eu','reg-keys':['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUrQ1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnWN1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGvTPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ==']}
    test_dict = {'hrn':'onelab.upmc.aaaa','email':'bbbb@onelab.eu'}
    print(Registry.create(user_dict, 'user'))
    print(Registry.update(test_dict,'user'))
    print(Registry.get('onelab.upmc.aaaa'))

    print("=====user test(upper)=======")
    user_dict = {'hrn':'onelab.inria.aaaa','email':'aaaa@onelab.eu','reg-keys':['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUrQ1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnWN1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGvTPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ==']}
    test_dict = {'hrn':'onelab.inria.aaaa','email':'bbbb@onelab.eu'}
    print(Registry.create(user_dict, 'user'))
    print(Registry.update(test_dict, 'user'))
    print(Registry.get('onelab.inria.aaaa'))

    print("=====authority test=======")
    auth_dict = {'hrn':'onelab.upmc.authx', 'reg-pis':[hrn]}
    print(Registry.create(auth_dict, 'authority'))
    auth_dict['reg-pis'] = [hrn, 'onelab.inria.aaaa', 'onelab.upmc.aaaa']
    print(Registry.update(auth_dict, 'authority'))
    print(Registry.get('onelab.upmc.authx'))

    print("=====authority test(upper)=======")
    auth_dict = {'hrn':'onelab.inria.authx', 'reg-pis':[hrn]}
    print(Registry.create(auth_dict, 'authority'))
    auth_dict['reg-pis'] = [hrn, 'onelab.inria.aaaa', 'onelab.upmc.aaaa']
    print(Registry.update(auth_dict, 'authority'))
    print(Registry.get('onelab.inria.authx'))

    print("=====slice test=======")
    slice_dict = {'hrn':'onelab.upmc.authx.slicex','reg-researchers':[hrn]}
    print(Registry.create(slice_dict, 'slice'))
    slice_dict = {'hrn':'onelab.upmc.authx.slicex','reg-researchers':[hrn,'onelab.inria.aaaa']}
    print(Registry.update(slice_dict, 'slice'))
    print(Registry.get('onelab.upmc.authx.slicex'))

    print("=====slice test(upper)=======")
    slice_dict = {'hrn':'onelab.inria.authx.slicex','reg-researchers':[hrn]}
    print(Registry.create(slice_dict, 'slice'))
    slice_dict['reg-researchers'] = [hrn,'onelab.upmc.aaaa']
    print(Registry.update(slice_dict, 'slice'))
    print(Registry.get('onelab.inria.authx.slicex'))
    
    print(Registry.user('onelab.inria.aaaa'))

    print("=====get slice=======")
    print(Registry.get('onelab.inria.authx.slicex', 'slice'))
    
    print("=====delete slice========")
    print(Registry.delete('onelab.inria.authx.slicex', 'slice'))
    print(Registry.delete('onelab.upmc.authx.slicex', 'slice'))

    print("=====delete users========")
    print(Registry.delete('onelab.inria.aaaa', 'user'))
    print(Registry.delete('onelab.upmc.aaaa', 'user'))

    print("=====delete authority=======")
    print(Registry.delete('onelab.upmc.authx', 'authority'))
    print(Registry.delete('onelab.inria.authx', 'authority'))

    #print(Registry.get('onelab.upmc.apitest.slicex', 'slice'))
    #print(AM.get('onelab.upmc.apitest.slicex', 'slice'))


def test_by_quan():
    url_am = "https://sfa3.planet-lab.eu:12346" 
    url_registry = "https://portal.onelab.eu:6080"
    #url_registry = "https://dev.myslice.info:12345"      

    path = "/root/.sfi/"
    pkey = path + "onelab.upmc.joshzhou16.pkey"
    cert = path + "onelab.upmc.joshzhou16.sscert"

    hrn = "onelab.upmc.joshzhou16"
    email = "joshzhou16@gmail.com"

    endpoint_registry = Endpoint(url=url_registry)
    endpoint_am = Endpoint(url=url_am)
    credential = Credential(email=email, hrn=hrn, private_key=pkey, certificate=cert)
    Registry = SfaReg(endpoint_registry, credential)
    AM = SfaAm(endpoint_am, Registry)
    
    
    #print(Registry.get(hrn))
    print("=====user test=======")
    user_dict = {'hrn':'onelab.upmc.apitest.aaaa','email':'aaaa@onelab.eu','reg-keys':['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUrQ1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnWN1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGvTPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ==']}
    test_dict = {'hrn':'onelab.upmc.apitest.aaaa','email':'bbbb@onelab.eu'}
    print(Registry.create(user_dict, 'user'))
    print(Registry.update(test_dict,'user'))
    pprint(Registry.get('onelab.upmc.apitest.aaaa'))

    print("=====slice test=======")
    slice_dict = {'hrn':'onelab.upmc.apitest.slicex','reg-researchers':[hrn]}
    print(Registry.create(slice_dict, 'slice'))
    slice_dict = {'hrn':'onelab.upmc.apitest.slicex','reg-researchers':[hrn, 'onelab.upmc.apitest.aaaa']}
    print(Registry.update(slice_dict, 'slice'))
    pprint(Registry.get('onelab.upmc.apitest.slicex'))
    print("=====get slice=======")
    print(Registry.get('onelab.upmc.apitest.slicex', 'slice'))
    

    #print(AM.list())

    #print("======delete slice=======")
    #AM.delete('onelab.upmc.apitest.slicex', 'slice')
    #print(AM.get('onelab.upmc.apitest.slicex', 'slice'))
    #pprint(Registry.get('onelab.upmc.apitest.aaaa'))    
    #print(Registry.delete('onelab.upmc.apitest.aaaa', 'user'))
    #print(Registry.delete('onelab.upmc.apitest.slicex', 'slice'))
    
    #print(AM.get('onelab.upmc.apitest.slicex', 'resource'))
    #record_dict = {'hrn': 'onelab.upmc.apitest.slicex', 'parsed':request_rspec, 'users': {}}#'users': [{'urn': 'urn:publicid:IDN+onelab:inria+user+aaaa', 'keys': ['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCgJ3h7WmEytfWcL0+dboFeKTLSYWlNpCijvcQHllWoP02ZAuWl7j0kqhHzssOOLhP830W3YuGoDrg+i8c8RbTa18Ei77VuOg3Mes/9jesFrY64pEv85ULEQD4gZ8r+qjVAW2cmiIe0Pe7hKNls7Dd0MBzXr34RbMAaB+EHy2s0dU5o4mtBmwmMzpIJ62pe1flRjyqq8UVnoRZTPW1aHrr0wNKoxavCrmHs/LX3G6Y/epSMdTIRBQEJblwdxzc62kZmRTBVif0PsNAqtxHNL79bO5OAaRqKe0wL8gYza/1wckD6UBxXZmBPGA3Au7piE34CCP+JFVS5RH21dxrlO6cH JoshPAT@portablerahman.rsr.lip6.fr']}]}
    #AM.create(record_dict, 'slice')
    #pprint(AM.get('onelab.upmc.apitest.slicex', 'slice'))
    #record_dict = {'hrn': 'onelab.upmc.apitest.slicey', 'parsed':request_rspec, 'users': [{'urn': 'urn:publicid:IDN+onelab:inria+user+aaaa', 'keys': []}]}
    #AM.get('onelab.upmc.apitest.slicey', 'slice')

    #AM.list('resource')
    
    

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('test_by_quan()')
    test_by_quan()
    #import timeit
    #print(timeit.repeat("test_by_quan()", setup="from __main__ import test_by_quan", number=1, repeat=3))
    #print(AM.version())
    #print(AM.list('lease')) 
    #print(AM.get(type='slice',hrn='onelab.upmc.slicex'))

    '''
    print("===== version =====")
    print(AM.version())
    print("===== list slice =====")
    print(AM.list('slice'))
    #print("===== list resource =====")
    #print(AM.list('resource'))
    print("===== list lease =====")
    print(AM.list('lease'))
    print("===== get hrn slice =====")
    print(AM.get('onelab.upmc.mobicom.exper_mobicom','slice'))
    print("===== get hrn resource =====")
    print(AM.get('iotlab.m3-83\.lille\.iot-lab\.info','resource'))
    print("===== get hrn lease =====")
    print(AM.get('iotlab.m3-83\.lille\.iot-lab\.info','lease'))

    exit

    record_dict = {}
    print("===== create hrn dict resource =====")
    print(AM.create('x',record_dict,'resource'))

    print("===== delete hrn slice =====")
    print(AM.delete('onelab.upmc.mobicom.exper_mobicom','slice'))

    print("===== read & parse rspec =====")
    with open (path + 'req_rspec_ple.xml', "r") as myfile:
        rspec = myfile.read()
    record_dict['parsed'] = xmltodict.parse(rspec)
    print("===== create hrn dict slice =====")
    print(AM.create('onelab.upmc.mobicom.exper_mobicom',record_dict,'slice'))
    
    print("===== update hrn {date} slice =====")
    d = datetime.datetime.utcnow() + datetime.timedelta(365/12)
    date = d.isoformat('T') + 'Z'
    print(type(date))
    print(AM.update('onelab.upmc.mobicom.exper_mobicom',{'expiration_date':date},'slice'))

    print("===== execute hrn action slice =====")
    print(AM.execute('onelab.upmc.mobicom.exper_mobicom', 'toto', 'slice'))
    print("===== execute hrn shutdown slice =====")
    print(AM.execute('onelab.upmc.mobicom.exper_mobicom', 'shutdown', 'slice'))

    print("===== delete hrn slice =====")
    print(AM.delete('onelab.upmc.mobicom.exper_mobicom','slice'))
    #print(AM.GetVersion())
    '''


