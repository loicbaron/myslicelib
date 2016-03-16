import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Users(Entities):
    pass

class User(Entity):
    _class = "User"
    _type = "user"
    _collection = "Users"
    
    def getAuthority(self):
        Authority = myslicelib.model.authority.Authority
        result = []
        for urn in self.attribute('users'):
            result += q(Authority).id(urn).get()
        return result

    def getPi_authorities(self):
        Authority = myslicelib.model.authority.Authority
        pi_auths = self.attribute('pi_authorities')
        # TODO parallel requests using MultiProcess     
        result = []
        for urn in pi_auths:
            result += q(Authority).id(urn).get()
        return result

    def getSlices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attribute('slices'):
            result += q(Slice).id(urn).get()
        return result


