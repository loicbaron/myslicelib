#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.slice import Slices, Slice
from myslicelib.model.authority import Authority
from myslicelib.query import q

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
                                                                    'name': 'apitest'
                                                                    })
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', res.dict()[0]['reg-urn'])

    def test_01_create_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').update({
                                                'reg-researchers': [hrn],
                                                })
        self.assertIsInstance(res, Slices)
        self.assertEqual('slice', res.dict()[0]['classtype'])
        self.assertIn(hrn, res.dict()[0]['reg-researchers'])

    def test_02_get_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').get()
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+slice+slicex', res.dict()[0]['reg-urn'])

    def test_03_update_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').update({
                                                'reg-researchers': [hrn, 'onelab.inria.aaaa'],
                                                })
        self.assertIn(hrn, res.dict()[0]['reg-researchers'])

    def test_04_get_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').get()
        for sli in res.dict():
            self.assertEqual('slice', sli['classtype'])
            self.assertEqual('onelab.upmc.authx', sli['authority'])

    def test_05_delete_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+slice+slicex').delete()
        self.assertTrue(res)

    def test_06_clear_up(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').delete()
        self.assertTrue(res)


    def test_slice_with_root_cred(self):
        res = self.q.id('urn:publicid:IDN+onelab:inria:authx+slice+slicex').update({
                                                        'reg-researchers': [hrn],
                                                        })
        self.assertEqual('urn:publicid:IDN+onelab:inria:authx+slice+slicex', res.dict()[0]['reg-urn'])
        self.assertIn(hrn, res.dict()[0]['reg-researchers'])
        res = self.q.id('urn:publicid:IDN+onelab:inria:authx+slice+slicex').delete()
        self.assertTrue(res)

    @unittest.expectedFailure
    def test_get_authority_from_user(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').get()
    
    def test_get_authority_from_root_authority(self):
        res = self.q.get()
        for auth in res.dict():
            self.assertEqual('slice', auth['classtype'])

if __name__ == '__main__':
    unittest.main()
