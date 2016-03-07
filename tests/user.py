#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.api import Api
from myslicelib.model.user import Users, User
from myslicelib.query import q

from myslicelib.error import MysNotUrnFormatError

from tests import s
from pprint import pprint

SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD3iRxbPseM1ZIvuZUr\
Q1p/4KKCqD38b09JFgB2k+aCiuaDKqjoQJ2Yi1MIhaI8QKn17ddZ2mnW\
N1YZuFlSaiD64rpQT6guoGSjXtQmHqq97lH037/LphRYs2BY6ZknlLGv\
TPcP2p4sEoMvOLCb8vPW1tKDFfM/RIuZjcn89irYjQ=="


class TestUser(unittest.TestCase):

    def setUp(self):
        self.q = q(User)
        
    def test_initial(self):
        self.assertIsNone(self.q._id)

    def test_id_is_urn(self):
        self.q.id('random_urn_string')
        self.assertRaises(MysNotUrnFormatError)

    def test_set_user(self):
        self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron')
        self.assertEqual('urn:publicid:IDN+onelab:upmc+user+lbaron', self.q._id)

    def test_create_user(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({
                                                'email':'loic.baron@gmail.com',
                                                })
        self.assertIsInstance(res, Users)
        self.assertEqual('user', res.dict()[0]['classtype'])
        self.assertEqual('loic.baron@gmail.com', res.dict()[0]['email'])

    def test_update_user(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({
                                                'email':'loic.baron.new@gmail.com',
                                                'reg-keys': [SSH_KEY],
                                                })
        self.assertEqual('loic.baron.new@gmail.com', res.dict()[0]['email'])
        self.assertIn(SSH_KEY, res.dict()[0]['reg-keys'])

    def test_delete_user(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').delete()
        self.assertTrue(res)

    def test_user_with_root_cred(self):
        res = self.q.id('urn:publicid:IDN+onelab:inria+user+lbaron').update({'email':'loic.baron@gmail.com'})
        self.assertEqual('loic.baron@gmail.com', res.dict()[0]['email'])
        res = self.q.id('urn:publicid:IDN+onelab:inria+user+lbaron').delete()
        self.assertTrue(res)

    def test_get_user_from_slice(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc:apitest+slice+slicex').get()
        self.assertEqual(Users(), res)

    def test_get_user_from_authority(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc+authority+sa').get()
        for user in res.dict():
            self.assertEqual('user', user['classtype'])
            self.assertEqual('onelab.upmc.sa', user['authority'])

    def test_get_user_from_root_authority(self):
        res = self.q.get()
        for user in res.dict():
            self.assertEqual('user', user['classtype'])


if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()
