#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q

from myslicelib.error import MysNotUrnFormatError

from tests import s
from tests import hrn

class TestAuthority(unittest.TestCase):

    def setUp(self):
        self.q = q(Authority)
        
    def test_initial(self):
        self.assertIsNone(self.q._id)

    def test_id_is_urn(self):
        self.q.id('random_urn_string')
        self.assertRaises(MysNotUrnFormatError)

    def test_id_authority(self):
        self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa')
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', self.q._id)

    def test_01_create_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                'reg-pis': [hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        self.assertEqual('authority', res.dict()[0]['classtype'])
        self.assertIn(hrn, res.dict()[0]['reg-pis'])

    def test_02_get_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').get()
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', res.dict()[0]['reg-urn'])

    def test_03_update_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                'reg-pis': ['onelab.upmc.joshzhou16', hrn],
                                                })
        self.assertIn('onelab.upmc.joshzhou16', res.dict()[0]['reg-pis'])

    def test_04_delete_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').delete()
        self.assertTrue(res)

    def test_authority_with_root_cred(self):
        res = self.q.id('urn:publicid:IDN+onelab:inria:authx+authority+sa').update({
                                                'reg-pis': [hrn],
                                                })
        self.assertEqual('urn:publicid:IDN+onelab:inria:authx+authority+sa', res.dict()[0]['reg-urn'])
        res = self.q.id('urn:publicid:IDN+onelab:inria:authx+authority+sa').delete()
        self.assertTrue(res)
        
    @unittest.expectedFailure
    def test_get_authority_from_slice(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()

    @unittest.expectedFailure
    def test_get_authority_from_user(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').get()

    def test_get_authority_from_root_authority(self):
        res = self.q.get()
        for auth in res.dict():
            self.assertEqual('authority', auth['classtype'])


if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()

