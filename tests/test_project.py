#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.project import Projects , Project
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from myslicelib.error import MysNotUrnFormatError

from tests import s
from tests import hrn


class TestProject(unittest.TestCase):

    def setUp(self):
        self.q = q(Project)
        
    def test_initial(self):
        self.assertIsNone(self.q._id)

    def test_id_is_urn(self):
        self.q.id('random_urn_string')
        self.assertRaises(MysNotUrnFormatError)

    def test_id_project(self):
        self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa')
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', self.q._id)

    def test_01_create_project(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                'reg-pis': [hrn],
                                                })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.attribute('pi_users'))

    def test_02_get_project(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').get()
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)

    def test_03_update_project(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                'reg-pis': ['onelab.upmc.joshzhou16', hrn],
                                                })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.attribute('pi_users'))
            self.assertIn(hrn_to_urn('onelab.upmc.joshzhou16', 'user'), auth.attribute('pi_users'))

    def test_04_delete_project(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').delete()
        self.assertTrue(res)

    def test_project_with_root_cred(self):
        res = self.q.id('urn:publicid:IDN+onelab:inria:authx+authority+sa').update({
                                                'reg-pis': [hrn],
                                                })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:inria:authx+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.attribute('pi_users'))
            res = self.q.id('urn:publicid:IDN+onelab:inria:authx+authority+sa').delete()
            self.assertTrue(res)
        
    @unittest.expectedFailure
    def test_get_project_from_slice(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()

    @unittest.expectedFailure
    def test_get_project_from_user(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').get()

    @unittest.expectedFailure
    def test_get_project_from_authority(self):
        with self.assertRaises(MysNotImplementedError):
            self.q.id('urn:publicid:IDN+onelab:inria+authority+sa')

if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()

