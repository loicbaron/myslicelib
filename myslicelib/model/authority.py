import myslicelib

from copy import copy
from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Authorities(Entities):
    pass

class Authority(Entity):
    _class = "Authority"
    _collection ="Authorities"

    def getUsers(self, pis = False):
        User = myslicelib.model.user.User
        result = []
        if pis:
            for urn in self.attribute('pi_users'):
                result += q(User).id(urn).get()
        else:
            for urn in self.attribute('users'):
                result += q(User).id(urn).get()
        return result

    def getSlices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attribute('slices'):
            result += q(Slice).id(urn).get()
        return result

    def addPi(self, user):
        self.pi_users.append(user.id)
        return self

    def removePi(self, user):
        self.pi_users = set(self.pi_users) - set(user.id)
        return self
