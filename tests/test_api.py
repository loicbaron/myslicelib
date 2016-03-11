#!/usr/bin/env python3.5
import sys
import unittest

from pprint import pprint
from myslicelib.api import Api
from myslicelib.model.user import Users, User
from myslicelib.model.resource import Resource
from myslicelib.query import q
from myslicelib.error import MysNotUrnFormatError
from tests.time import timeit
from tests import s

class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = Api(s.endpoints, s.credential)

    def test_version(self):
        res = self.api.version()
        #pprint(res)
        #self.assertEqual('1.0', res['myslicelib']['version'])
    
    def test_resources(self):
        qr= q(Resource)
        res = qr.get() 
        #print(res)

if __name__ == '__main__':
    unittest.main()
    # import time
    # start_time = time.time()
    # qr= q(Resource)
    # res = qr.get()
    # print(time.time()-start_time)