from myslicelib.model import Entities, Entity

class Leases(Entities):
    pass

class Lease(Entity):
    _class = "Lease"
    _collection = "Leases"
