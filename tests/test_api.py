#!/usr/bin/env python3.5
import sys
import unittest

from myslicelib.api import Api
from myslicelib.model.user import Users, User
from myslicelib.model.resource import Resource
from myslicelib.query import q
from myslicelib.error import MysNotUrnFormatError

from tests import s

class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = Api(s.endpoints, s.credential)

    def test_version(self):
        res = self.api.version()
        #print(res)
        #self.assertEqual('1.0', res['myslicelib']['version'])
    
    def test_resources(self):
        qr = q(Resource)
        res = qr.get()
        #print(res)
if __name__ == '__main__':
    unittest.main()