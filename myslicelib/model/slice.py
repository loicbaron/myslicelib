from myslicelib.model import Entities, Entity

class Slices(Entities):
    pass

class Slice(Entity):
    _class = "Slice"
    _collection = "Slices"

    def __str__(self):
        return self.name

