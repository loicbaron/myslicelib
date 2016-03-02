from myslicelib.model import Entities, Entity

class Authorities(Entities):
    pass

class Authority(Entity):

    @property
    def users(self):
        pass

    @property
    def projects(self):
        pass

class User(Entity):

    @property
    def slices(self):
        pass

class Project(Entity):

    @property
    def slices(self):
        pass

class Slice(Entity):

    def __str__(self):
        return self.name

    @property
    def users(self):
        pass



