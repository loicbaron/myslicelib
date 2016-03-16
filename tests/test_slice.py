#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.slice import Slices, Slice
from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError

from tests import s
from tests import hrn

class TestSlice(unittest.TestCase):

    def setUp(self):
        self.q = q(Slice)
        
    def test_initial(self):
        self.assertIsNone(self.q._id)

    def test_id_is_urn(self):
        self.q.id('random_urn_string')
        self.assertRaises(MysNotUrnFormatError)

    def test_id_slice(self):
        self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex')
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+slice+slicex', self.q._id)

    def test_00_create_auth(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                                    'name': 'Aa.pitest'
                                                                    })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)

    def test_01_create_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').update({
                                                'users': [hrn],
                                                })
        self.assertIsInstance(res, Slices)
        for sli in res:
            self.assertIn(hrn_to_urn(hrn, 'user'), sli.users)

    def test_02_get_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').get()       
        for sli in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+slice+slicex', sli.id)

    def test_03_update_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').update({
                                                'users': [hrn, 'onelab.inria.aaaa'],
                                                })
        for sli in res:
            self.assertIn(hrn_to_urn(hrn, 'user'), sli.users)
    
    def test_04_delete_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').delete()
        self.assertTrue(res)

    def test_05_clear_up(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').delete()
        self.assertTrue(res)

    # def test_slice_with_root_cred(self):
    #     res = self.q.id('urn:publicid:IDN+onelab:inria:authx+slice+slicex').update({
    #                                                     'reg-researchers': [hrn],
    #                                                     })
    #     self.assertEqual(res, Slices)
    #     for sli in res:
    #         self.assertEqual('urn:publicid:IDN+onelab:inria:authx+slice+slicex', sli.id)
    #         self.assertIn(hrn_to_urn(hrn, 'user'), sli.attribute('users'))
    #     res = self.q.id('urn:publicid:IDN+onelab:inria:authx+slice+slicex').delete()
    #     self.assertTrue(res)

    @unittest.expectedFailure
    def test_get_authority_from_user(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').get()
    
    # def test_get_authority_from_root_authority(self):
    #     res = self.q.get()
    #     for auth in res:
    #         self.assertIsNone 

if __name__ == '__main__':
    unittest.main()
