import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Projects(Entities):
    pass

class Project(Entity):
    _class = "Authority"
    _type = "authority"
    _collection = "Projects"

    def getUsers(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('users'):
            result += q(User).id(urn).get()
        return result

    def getPi_users(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('pi_users'):
            result += q(User).id(urn).get()
        return result

    def getSlices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attribute('slices'):
            result += q(Slice).id(urn).get()
        return result