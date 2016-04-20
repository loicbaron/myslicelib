#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.user import Users, User
from myslicelib.model.resource import Resources, Resource
from myslicelib.model.slice import Slices, Slice
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from tests import s
from tests import hrn

exec_user = q(User).id(hrn_to_urn(hrn,'user')).get().first()

class TestSlice(unittest.TestCase):

    def setUp(self):
        sli = Slice()
        self.assertIsInstance(sli, Slice)

    def test_addUser_and_addResources(self):
        
        # create slice
        sli = Slice()
        sli.shortname = 'slicetest'
        sli.authority = 'onelab.upmc.apitest'

        # add user 
        usr = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
        sli.addUser(usr)
        sli.addUser(exec_user)
        
        # add resources
        res = q(Resource).filter('country', 'Germany').filter('version', 'f22').get()
        sli.addResources(res)
        
        result = sli.save()

        # check if successful
        '''
        result = {  'data': [   
                                # AM
                                {
                                    'resources': [{resource1}, {resouce2}]
                                    'leases': []
                                    }
                                # Reg
                                {
                                    'hrn':..., 'users':...
                                    }
                                ]
                    'errors': 'xxxxx'
                    }
        '''

        for d in result['data']:
            if 'users' in d:
                self.assertIn(usr.id, d['users'])
            if 'resources' in d:
                self.assertIsNotNone(d['resources'])

if __name__ == '__main__':
    unittest.main()

