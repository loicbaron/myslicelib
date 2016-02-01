
class Entity(object):
    attributes = []

    def __init__(self, data = None):
        if data :
            self.attributes = data

    def __getattr__(self, name):
        if name in self.attributes:
            return self.attributes[name]
        else :
            raise AttributeError

    def save(self):
        raise NotImplementedError('Not implemented')

class Entities(set):

    def first(self):
        if len(self) > 0:
            return iter(self).next()

    def count(self):
        return len(self)

    def empty(self):
        if len(self) > 0:
            return True
        else:
            return False

    @property
    def ids(self):
        ret = []
        for e in self:
            ret.append(e.id)
        return ret