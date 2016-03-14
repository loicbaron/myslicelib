import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Users(Entities):
    pass

class User(Entity):
    _class = "User"
    _collection = "Users"
    
    @property
    def authority(self):
        Authority = myslicelib.model.authority.Authority
        result = []
        for urn in self.attribute('users'):
            result += q(User).id(urn).get()
        return result

    @authority.setter
    def authority(self, value):
        raise NotImplementedError('Cannot change authority')

    @property
    def pi_authorities(self):
        Authority = myslicelib.model.authority.Authority
        pi_auths = self.attribute('pi_authorities')
        # TODO parallel requests using MultiProcess     
        result = []
        for urn in pi_auths:
            result += q(Authority).id(urn).get()
        return result

    @pi_authorities.setter
    def pi_authorities(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.setattribute('pi_authorities', value)
        # TODO: to really update these

    @property
    def slices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attribute('slices'):
            result += q(Slice).id(urn).get()
        return result

    @slices.setter
    def slices(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.setattribute('slices', value)
        # TOD0: SFAAM UPDATE

