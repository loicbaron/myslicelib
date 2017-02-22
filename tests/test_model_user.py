#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.user import Users, User

from tests import s


PKEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUr\
Q1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnW\
N1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGv\
TPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ=="

class TestUser(unittest.TestCase):

    created_user = None

    def setUp(self):
        u = User()
        self.assertIsInstance(u, User)

    def test_1_setter_id(self):
        u = User()
        u.id = 'urn:publicid:IDN+onelab:upmc+user+lbaron'
        self.assertEqual(u.id, 'urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual(u.authority, 'urn:publicid:IDN+onelab:upmc+authority+sa')
        self.assertEqual(u.hrn, 'onelab.upmc.lbaron')
        self.assertEqual(u.shortname, 'lbaron')

    def test_2_setter_authority(self):
        u = User()
        u.hrn = 'onelab.upmc.lbaron'
        self.assertEqual(u.id, 'urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual(u.authority, 'urn:publicid:IDN+onelab:upmc+authority+sa')
        self.assertEqual(u.hrn, 'onelab.upmc.lbaron')
        self.assertEqual(u.shortname, 'lbaron')

    def test_3_setter_auth_and_shrtnm(self):
        u = User()
        u.authority = 'urn:publicid:IDN+onelab:upmc+authority+sa'
        u.shortname = 'lbaron'
        self.assertEqual(u.id, 'urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual(u.authority, 'urn:publicid:IDN+onelab:upmc+authority+sa')
        self.assertEqual(u.hrn, 'onelab.upmc.lbaron')
        self.assertEqual(u.shortname, 'lbaron')

    def test_4_save(self):
        u = User()
        u.hrn = 'onelab.upmc.lbaron'
        u.email = 'apitest@onelab.eu'
        u.keys = [PKEY]
        # test save
        res = u.save()
        usrdata, errors = res['data'][0], res['errors']
        self.assertEqual(res['errors'], [])
        self.assertEqual(usrdata['hrn'], 'onelab.upmc.lbaron')
        self.assertEqual(usrdata['email'], 'apitest@onelab.eu')
        self.assertEqual(usrdata['keys'], [PKEY])
        self.assertIsNotNone(usrdata['certificate'])
        self.__class__.created_user = User(usrdata)

    def test_5_delete(self):
        u = self.created_user
        # test delete
        res = u.delete()
        self.assertEqual(res, {'errors': [], 'data': []})


if __name__ == '__main__':
    unittest.main()
