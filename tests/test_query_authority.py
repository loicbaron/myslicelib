#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.authority import Authority, Authorities
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from myslicelib.error import MysNotUrnFormatError

from tests import s
from tests import hrn


class TestAuthority(unittest.TestCase):

    def test_id_is_urn(self):
        a = q(Authority).id('random_urn_string')
        # TODO: Check errors in a.logs 
        self.assertRaises(MysNotUrnFormatError)

    def test_id_authority(self):
        a = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa')
        self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', a._id)

    def test_01_create_authority(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa').update({
                                                'pi_users': [hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)

    def test_02_get_authority(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa').get()
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)

    def test_03_update_authority(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa').update({
                                                'pi_users': ['onelab.upmc.joshzhou16', hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)
            self.assertIn(hrn_to_urn('onelab.upmc.joshzhou16', 'user'), auth.pi_users)

    def test_04_delete_authority(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa').delete()
        self.assertEqual({'errors':[],'data':[]}, res)

    def test_authority_with_root_cred(self):
        res = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa').update({
                                                'pi_users': [hrn],
                                                })
        self.assertIsInstance(res, Authorities)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:coucou+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)
            res = q(Authority).id('urn:publicid:IDN+onelab:coucou+authority+sa').delete()
            self.assertEqual({'errors':[],'data':[]}, res)
        
    # def test_get_authority_from_root_authority(self):
    #     res = q(Authority).get()
    #     for auth in res:
    #         self.assertIsNotNone(auth.getAttribute('pi_users'))

if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()

