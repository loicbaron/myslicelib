import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Authorities(Entities):
    pass

class Authority(Entity):
    _class = "Authority"
    _collection ="Authorities"

    @property
    def users(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attributes()['users']:
            result += q(User).id(urn).get()
        return result

    @users.setter
    def users(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.attributes()['users'] = value

    @property
    def pi_users(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attributes()['pi_users']:
            result += q(User).id(urn).get()
        return result

    @pi_users.setter
    def pi_users(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.attributes()['pi_users'] = value

    @property
    def slices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attributes()['slices']:
            result += q(Slice).id(urn).get()
        return result

    @slices.setter
    def slices(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.attributes()['slices'] = value
        # TOD0: SFAAM UPDATE
