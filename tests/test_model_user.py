#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.user import Users, User

class TestUser(unittest.TestCase):

    def setUp(self):
        u = User()
        self.assertIsInstance(u, User)

    def test_setter_id(self):
        u = User()
        u.id = 'urn:publicid:IDN+onelab:upmc+user+lbaron'
        self.assertEqual(u.id, 'urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual(u.authority, 'onelab.upmc')
        self.assertEqual(u.hrn, 'onelab.upmc.lbaron')
        self.assertEqual(u.shortname, 'lbaron')

    def test_setter_authority(self):
        u = User()
        u.hrn = 'onelab.upmc.lbaron'
        self.assertEqual(u.id, 'urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual(u.authority, 'onelab.upmc')
        self.assertEqual(u.hrn, 'onelab.upmc.lbaron')
        self.assertEqual(u.shortname, 'lbaron')

    def test_setter_auth_and_shrtnm(self):
        u = User()
        u.authority = 'onelab.upmc'
        u.shortname = 'lbaron'
        self.assertEqual(u.id, 'urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual(u.authority, 'onelab.upmc')
        self.assertEqual(u.hrn, 'onelab.upmc.lbaron')
        self.assertEqual(u.shortname, 'lbaron')



if __name__ == '__main__':
    unittest.main()