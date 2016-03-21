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
        super().__init__(data)
        if data is None:
            self.users = []
            self.geni_users = []
            self.resources = []
            self.leases = []

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
       
    def addUser(self, user):
        self.users.append(user.hrn)
        self.geni_users.append({'urn':user.id,'keys':user.keys,'email':user.email})
        return self
    
    def removeUser(self, user):
        self.geni_users = list(filter(lambda x: x['urn']==user.id, self.geni_users))
        self.users = list(set(self.users) - set(user.hrn))
        return self
    
    def addResource(self, resource):
        self.resources.append(resource.attributes())
        return self

    def addResources(self, resources):
        for r in resources:
            self.addResource(r)
        return self

    def removeResource(self, resource):
        self.resources = list(filter(lambda x: x['id']==resource.id, self.resources))
        return self

    def removeResources(self):
        self.resources = [] 
        return self

    def addLease(self, lease):
        self.leases.append(lease.attributes())
        return self

    def removeLease(self, lease):
        raise NotImplemented("not implemented yet") 

    def removeLeases(self, lease):
        self.leases = []
        return self
