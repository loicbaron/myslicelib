#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.project import Projects , Project
from myslicelib.query import q
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError

from tests import s
from tests import hrn


class TestProject(unittest.TestCase):

    def test_id_is_urn(self):
        p = q(Project).id('random_urn_string')
        # TODO: check errors in p.logs
        self.assertRaises(MysNotUrnFormatError)

    def test_id_project(self):
        p = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa')
        self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', p._id)

    def test_01_create_project(self):
        res = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                'pi_users': [hrn],
                                                })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)

    def test_02_get_project(self):
        res = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').get()
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)

    def test_03_update_project(self):
        res = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').update({
                                                'pi_users': ['onelab.upmc.joshzhou16', hrn],
                                                })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:upmc:authx+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)
            self.assertIn(hrn_to_urn('onelab.upmc.joshzhou16', 'user'), auth.pi_users)

    def test_04_delete_project(self):
        res = q(Project).id('urn:publicid:IDN+onelab:upmc:authx+authority+sa').delete()
        self.assertEqual({'errors':[],'data':[]}, res)

    def test_project_with_root_cred(self):
        res = q(Project).id('urn:publicid:IDN+onelab:inria:authx+authority+sa').update({
                                                'pi_users': [hrn],
                                                })
        self.assertIsInstance(res, Projects)
        for auth in res:
            self.assertEqual('urn:publicid:IDN+onelab:inria:authx+authority+sa', auth.id)
            self.assertIn(hrn_to_urn(hrn, 'user'), auth.pi_users)
            res = q(Project).id('urn:publicid:IDN+onelab:inria:authx+authority+sa').delete()
            self.assertEqual({'errors':[],'data':[]}, res)
        
if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()
