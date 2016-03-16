import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Slices(Entities):
    pass

class Slice(Entity):
    _class = "Slice"
    _type = "slice"
    _collection = "Slices"

    def __init__(self, data = None):
        if data is None:
            self.users = []
            self.resources = []
            self.leases = []

        super().__init__(data)

    def getUsers(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('users'):
            result += q(User).id(urn).get()
        return result

    def getAuthority(self):
        Authority = myslicelib.model.authority.Authority
        urn = self.attribute('authority')
        return q(Authority).id(urn).get()
        
