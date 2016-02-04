#!/bin/env python3

'''
DISCLAIMER: this is a file to test during development, needs to be removed
'''
import datetime
import xmltodict
from myslicelib.api.sfareg import SfaReg
from myslicelib.api.sfaam import SfaAm

if __name__ == '__main__':

    path = "/root/.sfi/"
    pkey = path + "onelab.upmc.loic_baron.pkey"
    hrn = "onelab.upmc.loic_baron"
    email = "loic.baron@lip6.fr"
    cert = path + "onelab.upmc.loic_baron.sscert"
    url_am = "http://sfa3.planet-lab.eu:12346"
    #url = "https://nitlab.inf.uth.gr:8001/RPC2"
    #url_registry = "http://dev.myslice.info:12345"
    url_registry = "http://portal.onelab.eu:12345"  

    Registry = SfaReg(url=url_registry, pkey=pkey, certfile=cert, hrn=hrn) 
    AM = SfaAm(url=url_am, pkey=pkey, certfile=cert, reg=Registry)

    #print(Registry.version())
    #print(Registry.get(hrn))
    #print(Registry.list())
    #print(Registry.list("onelab.upmc"))

    #user_dict = {'hrn':'onelab.upmc.aaaa','email':'aaaa@onelab.eu','reg-keys':['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUrQ1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnWN1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGvTPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ==']}

    '''
    test_dict = {'hrn':'onelab.upmc.aaaa','email':'bbbb@onelab.eu','type':'user'}

    print(Registry.create(user_dict, 'user'))
    print(Registry.remove('onelab.upmc.aaaa', user_dict, 'user'))

    print(AM.version())
    print(AM.list('resource'))
    print(AM.get(type='slice',hrn='onelab.upmc.openlabdemo'))
    '''
    #print(Registry.create(user_dict, 'user'))
    #print(Registry.delete('onelab.upmc.aaaa', 'user'))
    #user_dict = {'hrn':'onelab.upmc.aaaa','email':'bbbbb@onelab.eu'}    
    #print(Registry.update(user_dict,'user'))
    #print(Registry.get('onelab.upmc.aaaa'))

    print("===== version =====")
    print(AM.version())
    print("===== list slice =====")
    print(AM.list('slice'))
    print("===== list resource =====")
    print(AM.list('resource'))
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
    
    exit
    with open (cert, "r") as myfile:
        data = myfile.read()

    credentials = Registry.GetSelfCredential(data, hrn, 'user')
    
    api_options = {
        'geni_rspec_version': {'type': 'GENI', 'version': '3'},
        'list_leases': 'all'
    }
    #print AM.ListResources([credentials], api_options)

    # {'output': '', 'geni_api': 3, 'code': {'am_type': 'sfa', 'geni_code': 0, 'am_code': None}, 'value': rspec }

    # resources = q('testbed.Resource').execute()
    # print resources.first().hostname
    # for r in resources:
    #     print r.hostname
    #     print r.hrn

    # print "Test"
    # auth = {'AuthMethod': 'password', 'Username': 'cscognamiglio@gmail.com', 'AuthString': 'demo'}
    # url = 'https://test.myslice.info:7080/'
    # api = Api(auth, url)


