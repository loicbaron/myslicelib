#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.slice import Slices, Slice
from myslicelib.model.user import Users, User
from myslicelib.model.authority import Authorities, Authority
from myslicelib.model.project import Projects, Project
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError

from tests import s
from tests import hrn

from pprint import pprint

user = q(User).id(hrn_to_urn(hrn,'user')).get().first()

class TestSlice(unittest.TestCase):

    def test_id_is_urn(self):
        sl = q(Slice).id('random_urn_string')
        # Check errors in sl.logs
        self.assertRaises(MysNotUrnFormatError)

    def test_id_slice(self):
        sl = q(Slice).id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex')
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+slice+slicex', sl._id)

    def test_01_create_auth(self):
        res = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                                    'name': 'Apitest'
                                                                    })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)

    def test_02_create_slice(self):
        res = q(Slice).id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').update({
                                                'users': [hrn],
                                                'geni_users': [{'urn':user.id,'keys':user.keys,'email':user.email}],
                                                'resources': [],
                                                })
        self.assertIsInstance(res, Slices)
        for sli in res:
            self.assertIn(hrn_to_urn(hrn, 'user'), sli.users)

    def test_03_get_slice(self):
        res = q(Slice).id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').get()       
        for sli in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+slice+slicex', sli.id)

    def test_04_update_slice(self):
        res = q(Slice).id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').update({
                                                'users': [hrn, 'onelab.inria.aaaa'],
                                                'geni_users': [{'urn':user.id,'keys':user.keys,'email':user.email}],
                                                'resources': [],
                                                })
        for sli in res:
            self.assertIn(hrn_to_urn(hrn, 'user'), sli.users)
    
    def test_05_delete_slice(self):
        res = q(Slice).id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').delete()
        #pprint(res)
        self.assertEqual({'errors':[],'data':[]}, res)

    def test_06_clear_up(self):
        res = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').delete()
        self.assertEqual({'data': [], 'errors': []}, res)

    def test_slice_with_root_cred(self):
        q(Project).id('urn:publicid:IDN+onelab:inria:authx+authority+sa').update({
                                                                    'name': 'Apitest'
                                                                    })
        res = q(Slice).id('urn:publicid:IDN+onelab:inria:authx+slice+slicex').update({
                                                        'users': [hrn],
                                                        'geni_users': [{'urn':user.id,'keys':user.keys,'email':user.email}],
                                                        'resources': [],
                                                        })

        #pprint(res)
        self.assertIsInstance(res, Slices)
        for sli in res:
            self.assertEqual('urn:publicid:IDN+onelab:inria:authx+slice+slicex', sli.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), sli.users)

        res = q(Slice).id('urn:publicid:IDN+onelab:inria:authx+slice+slicex').delete()
        self.assertEqual({'data': [], 'errors': []}, res)
        q(Project).id('urn:publicid:IDN+onelab:inria:authx+authority+sa').delete()


    #def test_get_authority_from_user(self):
    #    with self.assertRaises(MysNotImplementedError):
    #        res = q(Slice).id('urn:publicid:IDN+onelab:upmc+user+lbaron').get()
    
    # def test_get_authority_from_root_authority(self):
    #     res = q(Slice).get()
    #     for auth in res:
    #         self.assertIsNone 

if __name__ == '__main__':
    unittest.main()
