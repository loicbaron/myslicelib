import unittest
from myslicelib.api import Api

from myslicelib.model.user import Users, User
from myslicelib.query import q
from myslicelib.error import MysNotUrnFormatError

from tests import s


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

    def test_get_user(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').update({'email':'loic.baron@gmail.com'})
        #self.assertEqual(res)

    def test_delete_user(self):
        res = self.q.id('urn:publicid:IDN+onelab:upmc+user+lbaron').delete()



if __name__ == '__main__':
    #print(q(User).get())
    unittest.main()
