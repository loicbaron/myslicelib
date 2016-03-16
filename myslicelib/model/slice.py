import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Slices(Entities):
    pass

class Slice(Entity):
    _class = "Slice"
    _type = "slice"
    _collection = "Slices"

    # def __str__(self):
    #     return self.name

    @property
    def users(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('users'):
            result += q(User).id(urn).get()
        return result

    @users.setter
    def users(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.setattribute('users', value)

    @property
    def authority(self):
        Authority = myslicelib.model.authority.Authority
        urn = self.attribute('authority')
        return q(Authority).id(urn).get()

    @authority.setter
    def authority(self, value):
        raise NotImplementedError('Cannot change authority')

    @property
    def resources(self):
        return self.attribute('resources')

    @resources.setter
    def resources(self):
        pass

    @property
    def leases(self):
        return self.attribute('leases')

    @leases.setter
    def leases(self):
        pass



