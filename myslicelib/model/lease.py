from myslicelib.model import Entities, Entity

class Leases(Entities):
    pass

class Lease(Entity):
    _class = "Lease"
    _type = "lease"
    _collection = "Leases"

    def __init__(self, data = None):
        super().__init__(data)
        if data is None:
            self.resources = []

    def addResource(self, resource):
        self.resources.append(resource.id)
        return self

    def addResources(self, resources):
        for r in resources:
            self.addResource(r)
        return self

    def removeResource(self, resource):
        self.resources = list(set(self.resources) - set(resource.id))
        return self

    def removeResources(self):
        self.resources = [] 
        return self

