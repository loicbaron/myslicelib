#!/bin/env python3

'''
DISCLAIMER: this is a file to test during development, needs to be removed
'''
from myslicelib.api.sfa import Api

if __name__ == '__main__':

    path = "/Users/moray/Sites/upmc/"
    pkey = path + "cscognamiglio_onelab.pkey"
    hrn = "onelab.upmc.cscognamiglio"
    email = "cscognamiglio@gmail.com"
    cert = path + "cscognamiglio_onelab.cert"
    url_am = "http://sfa3.planet-lab.eu:12346"
    #url = "https://nitlab.inf.uth.gr:8001/RPC2"
    url_registry = "http://portal.onelab.eu:12345"
    url_registry = "http://sfa3.planet-lab.eu:12345"
    Registry = Api(url=url_registry, pkey=pkey, certfile=cert)
    AM = Api(url=url_am, pkey=pkey, certfile=cert)

    print AM.GetVersion()
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


