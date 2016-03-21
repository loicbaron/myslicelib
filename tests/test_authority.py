#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.authority import Authority, Authorities
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from myslicelib.error import MysNotUrnFormatError

from tests import s
from tests import hrn


class TestProject(unittest.TestCase):

    def setUp(self):
        self.q = q(Authority)
        
    def test_initial(self):
        self.assertIsNone(self.q._id)

    def test_id_is_urn(self):
        self.q.id('random_urn_string')
        self.assertRaises(MysNotUrnFormatError)

    def test_id_authority(self):
        self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa')
        self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', self.q._id)

    def test_01_create_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa').update({
                                                'pi_users': [hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)

    def test_02_get_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa').get()
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)

    def test_03_update_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa').update({
                                                'pi_users': ['onelab.upmc.joshzhou16', hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)
            self.assertIn(hrn_to_urn('onelab.upmc.joshzhou16', 'user'), auth.pi_users)

    def test_04_delete_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa').delete()
        self.assertEqual([], res)

    def test_authority_with_root_cred(self):
        res = self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa').update({
                                                'pi_users': [hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)
            res = self.q.id('urn:publicid:IDN+onelab:coucou+authority+sa').delete()
            self.assertEqual([], res)
        
    # def test_get_authority_from_root_authority(self):
    #     res = self.q.get()
    #     for auth in res:
    #         self.assertIsNotNone(auth.attribute('pi_users'))

if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()

