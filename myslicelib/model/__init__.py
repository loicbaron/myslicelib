from typing import Set

class Entity(object):

    _attributes = []

    def __init__(self, data = None):

        if data :
            self._attributes = data

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        else :
            raise AttributeError

    def attributes(self):
        return self._attributes

    def save(self):
        raise NotImplementedError('Not implemented')

class Entities(Set[Entity]):

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

    def dict(self):
        '''

        :return:
        '''
        list = []
        for e in self:
            list.append(e.attributes())

        return list

    # def filter(self, key, value):
    #     self.f[key] = value
    #     return self
    #
    # def order(self, order):
    #     return self.sort(order)
    #
    # def sort(self, sort):
    #     return self.filter('-SORT', sort)
    #
    # def offset(self, offset):
    #     if offset > 0:
    #         return self.filter('-OFFSET', offset)
    #     return self
    #
    # def limit(self, limit):
    #     return self.filter('-LIMIT', limit)
    #
    # def gt(self, key, value):
    #     return self.filter('>' + key, value)
    #
    # def gte(self, key, value):
    #     return self.filter(']' + key, value)
    #
    # def lt(self, key, value):
    #     return self.filter('<' + key, value)
    #
    # def lte(self, key, value):
    #     return self.filter('[' + key, value)
    #

    @property
    def ids(self):
        ret = []
        for e in self:
            ret.append(e.id)
        return ret