from myslicelib import setup as s, Setup
from myslicelib.api import Api
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn

class Entity(object):
    _attributes = {}
    _type = 'entity'
    _api = None
    _generator = ['id', 'hrn', 'authority', 'shortname']

    def __init__(self, data = None):
        if self._attributes:
            self._attributes = {}
        if data:
            self._attributes = data

    def __repr__(self):
        return "%s" % (self.attributes())

    def __getattr__(self, name):
        return self.attribute(name)

    def __setattr__(self, name, value):
        self.setattribute(name, value)

    def attributes(self):
        return self._attributes

    def attribute(self, name):
        try:
            return self._attributes[name]
        except KeyError :
            raise AttributeError('Entity object has no attribute %s' % 'name')  
    
    def setattribute(self, name, value):
        if name != '_api':
            self._attributes[name] = value
        super().__setattr__(name, value)
        if name in self._generator:
            group = getattr(self, '_generate_with_' + name)()
            self._group_settaribute(group)

    def _group_settaribute(self, group):
        for k, v in group.items():
            super().__setattr__(k, v)
            self._attributes[k] = v

    def _generate_with_id(self):
        hrn = urn_to_hrn(self.id)[0]
        group = dict(
                hrn = hrn,
                authority = '.'.join(hrn.split('.')[:-1]),
                shortname = hrn.split('.')[-1]
                )
        return group

    def _generate_with_hrn(self):
        group = dict(
                id = hrn_to_urn(self.hrn, self._type),
                authority = '.'.join(self.hrn.split('.')[:-1]),
                shortname = self.hrn.split('.')[-1]
                )
        return group

    def _generate_with_shortname(self):
        if 'authority' in self._attributes:
            hrn = self.authority + '.' + self.shortname
            group = dict(
                hrn = hrn,
                id = hrn_to_urn(hrn, self._type)
                )
            return group
        return {}

    def _generate_with_authority(self):
        if 'shortname' in self._attributes:
            hrn = self.authority + '.' + self.shortname
            group = dict(
                hrn = hrn,
                id = hrn_to_urn(hrn, self._type)
                )
            return group
        return {}

    def dict(self):
        return self._attributes

    def clear(self):
        self._api = None
        self.attribute = {}

    def save(self, setup=None):

        if setup and isinstance(setup, Setup):
            _setup = setup
        else:
            _setup = s

        # using _type instead of _class as project is an authority in SFA Reg
        self._api = getattr(Api(_setup.endpoints, _setup.credential), self._type)()

        if not self.id:
            # id can be None it will be forged based on the attributes (hrn...)
            self.id = None

        res = self._api.update(self.id, self.attributes())

        result = {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }

        return result

    def delete(self, setup=None):

        if setup and isinstance(setup, Setup):
            _setup = setup
        else:
            _setup = s

        if not self.id:
            raise Exception("No element specified")

        # But it means errors will stay in logs until we use a new instance
        # using _type instead of _class as project is an authority in SFA Reg
        self._api = getattr(Api(_setup.endpoints, _setup.credential), self._type)()

        res = self._api.delete(self.id)
        
        result = {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }
        return result

class Entities(set):

    def first(self):
        if len(self) > 0:
            return next(iter(self))

    def count(self):
        return len(self)

    def empty(self):
        if len(self) > 0:
            return True
        else:
            return False

    def has(self, id):
        '''
        Returns true if element with id exists

        :param id:
        :return:
        '''
        return any(el.id == id for el in self)

    def hasErrors(self):
        if self.logs:
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

    def save(self):
        for e in self:
            e.save()

    def delete(self):
        for e in self:
            e.delete()

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
