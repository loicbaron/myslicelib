#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.model.user import Users, User
from myslicelib.query import q

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError

from tests import s

SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUr\
Q1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnW\
N1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGv\
TPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ=="


class TestUser(unittest.TestCase):

    def test_id_is_urn(self):
        u = q(User).id('random_urn_string')
        # TODO: Check errors in u.logs
        self.assertRaises(MysNotUrnFormatError)

    def test_id_user(self):
        u = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual('urn:publicid:IDN+onelab:upmc+user+lbaron', u._id)

    def test_01_create_user(self):
        res = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({
                                                'email':'loic.baron@gmail.com',
                                                })
        self.assertIsInstance(res, Users)
        for user in res:
            self.assertEqual('loic.baron@gmail.com', user.email)
            self.assertEqual([], user.keys)
            self.assertEqual('urn:publicid:IDN+onelab:upmc+user+lbaron', user.id)

    def test_02_get_user(self):
        res = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').get()
        for user in res:
            self.assertEqual('loic.baron@gmail.com', user.email)
            self.assertEqual([], user.keys)
            self.assertEqual('urn:publicid:IDN+onelab:upmc+user+lbaron', user.id)

    def test_03_update_user(self):
        res = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({
                                                'email':'loic.baron.new@gmail.com',
                                                'keys': [SSH_KEY],
                                                })
        for user in res:
            self.assertEqual('loic.baron.new@gmail.com', user.email)
            self.assertIn(SSH_KEY, user.keys)
            self.assertEqual('urn:publicid:IDN+onelab:upmc+user+lbaron', user.id)


    def test_04_delete_user(self):
        res = q(User).id('urn:publicid:IDN+onelab:upmc+user+lbaron').delete()
        self.assertEqual({'errors':[],'data':[]}, res)

    def test_user_with_root_cred(self):
        res = q(User).id('urn:publicid:IDN+onelab:inria+user+lbaron').update({'email':'loic.baron@gmail.com'})
        self.assertIsInstance(res, Users)
        for user in res:
            self.assertEqual('loic.baron@gmail.com', user.email)
            self.assertEqual('urn:publicid:IDN+onelab:inria+user+lbaron', user.id)
        res = q(User).id('urn:publicid:IDN+onelab:inria+user+lbaron').delete()
        from pprint import pprint
        pprint(res)
        self.assertEqual({'errors':[],'data':[]}, res)
        
    def test_get_user_from_slice(self):
        with self.assertRaises(MysNotImplementedError):
            res = q(User).id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()

    def test_get_user_from_authority(self):
        with self.assertRaises(MysNotImplementedError):
            res = q(User).id('urn:publicid:IDN+onelab:upmc+authority+sa').get()

    def test_get_user_from_root_authority(self):
        res = q(User).get()
        self.assertIsInstance(res, Users)
        for user in res:
            self.assertIsNotNone(user.attribute('pi_authorities'))

if __name__ == '__main__':
    unittest.main()
