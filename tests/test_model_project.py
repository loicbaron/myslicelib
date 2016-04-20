#!/usr/bin/env python3.5
import sys
import unittest

from pprint import pprint

from myslicelib.model.user import Users, User
from myslicelib.model.project import Projects, Project
from myslicelib.query import q

from tests import s

class TestProject(unittest.TestCase):

    def setUp(self):
        proj = Project()
        self.assertIsInstance(proj, Project)

    def test_addPi_and_isPi(self):
        # update the project
        proj = Project()
        proj.id = 'urn:publicid:IDN+onelab:upmc:apitest+authority+sa'
        usr = q(User).id('urn:publicid:IDN+onelab:upmc+user+loic_baron').get().first()
        proj.addPi(usr)
        proj.save()
        # check if successful
        proj = q(Project).id('urn:publicid:IDN+onelab:upmc:apitest+authority+sa').get().first()
        self.assertTrue(proj.isPi(usr))

if __name__ == '__main__':
    unittest.main()
