import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

from pprint import pprint

class Slices(Entities):
    pass

class Slice(Entity):
    _class = "Slice"
    _type = "slice"
    _collection = "Slices"

    def __init__(self, data = {}):
        data = data if data is not None else {}
        data['users'] = data.get('users', [])
        data['geni_users'] = data.get('geni_users', [])
        data['resources'] = data.get('resources', [])
        data['leases'] = data.get('leases', [])
        data['run_am'] = data.get('run_am', False)
        super().__init__(data)

    def getUsers(self, attribute=False):
        if attribute:
            return self.getAttribute('users')
        else:
            User = myslicelib.model.user.User
            result = []
            for urn in self.getAttribute('users'):
                result += q(User).id(urn).get()
            return result

    def getAuthority(self, attribute=False):
        if attribute:
            return self.getAttribute('authority')
        else:
            Authority = myslicelib.model.authority.Authority
            urn = self.getAttribute('authority')
            return q(Authority).id(urn).get()
       
    def addUser(self, user):
        self.appendAttribute('users', user.id)
        self.appendAttribute('geni_users', {'urn':user.id,'keys':user.keys,'email':user.email})
        self.setAttribute('run_am', True)
        return self
    
    def removeUser(self, user):
        self.setAttribute('geni_users', list(filter(lambda x: x['urn']!=user.id, self.geni_users)))
        self.setAttribute('users', list(set(self.getAttribute('users')) - set([user.id])))
        self.setAttribute('run_am', True)
        return self
    
    def addResource(self, resource):
        self.appendAttribute('resources', resource.getAttributes())
        self.setAttribute('run_am', True)
        return self

    def addResources(self, resources):
        for r in resources:
            self.addResource(r)
        return self

    def removeResource(self, resource):
        self.setAttribute('resources', list(filter(lambda x: x['id']!=resource.id, self.resources)))
        self.setAttribute('run_am', True)
        return self

    def removeResources(self):
        self.setAttribute('resources', [] )
        self.setAttribute('run_am', True)
        return self

    def addLease(self, lease):
        self.appendAttribute('leases', lease.getAttributes())
        self.setAttribute('run_am', True)
        return self

    def removeLease(self, lease):
        raise NotImplemented("not implemented yet") 

    def removeLeases(self, lease):
        self.setAttribute('leases', [])
        self.setAttribute('run_am', True)
        return self

    def save(self, setup=None):
        # check if we have the email
        if not self.hasAttribute('shortname'):
            raise Exception('Slice shortname must be specified')

        if not self.hasAttribute('authority'):
            raise Exception('Slice authority must be specified')

        return super().save(setup)
