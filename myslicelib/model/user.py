import myslicelib

from myslicelib import setup as s, Setup
from myslicelib.api import Api

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
        urn = self.attribute('authority')
        return q(Authority).id(urn).get()

    def getPiAuthorities(self):
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

    def getCredential(self, id, delegate_to=None, setup=None):
        return self.getCredentials(id, delegate_to, setup)

    def getCredentials(self, id=None, delegate_to=None, setup=None):

        if setup and isinstance(setup, Setup):
            _setup = setup
        else:
            _setup = s

        self._api = getattr(Api(_setup.endpoints, _setup.authentication), self._class.lower())()

        if id:
            ids = [id]
        else:
            ids =[]
            ids.append(self.id)

            for urn in self.attribute('slices'):
                ids.append(urn)

            for urn in self.attribute('pi_authorities'):
                ids.append(urn)

        res = self._api.get_credentials(ids, delegate_to)
        self.credentials = res['data']
        self.logs = res['errors']

        return self
