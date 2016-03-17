from myslicelib import setup as s
from myslicelib.api import Api
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn

class Entity(object):
    _attributes = {}
    _type = 'entity'
    _api = None
    _flag = False
    _id = None
    _authority = None
    _shortname = None
    _hrn = None

    def __init__(self, data = None):
        if data :
            self._attributes = data

        self._api = getattr(Api(s.endpoints, s.credential), self._class.lower())()

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
            raise KeyError
    
    # XXX cant setattribute succuessfully
    def setattribute(self, name, value):
        if name != '_api':
            self._attributes[name] = value
        super().__setattr__(name, value)
    #     if not hasattr(self, name):
    #         self._attributes[name] = value
    #     else:
    #         self._attributes[name] = value
    #         super().__setattr__(name, value)

    def dict(self):
        return self._attributes

    def save(self):
        if not self.id:
            if self.hrn:
                self.id = hrn_to_urn(self.hrn, self._type)
            else:
                self.id = None
            
        res = self._api.update(self.id, self.attributes())
        
        return res

    def delete(self):
        if not self.id:
            raise Exception("No element specified")

        res = self._api.delete(self.id)

        return res

    @property
    def authority(self):
        return self._authority

    @authority.setter
    def authority(self, value):
        self._authority = value
        if self._hrn is None and self.shortname:
             self.hrn = value + self.shortname
        if self._id is None and self.hrn:
             self.id = hrn_to_urn(self.hrn, self._type)

    @property
    def shortname(self):
        return self._shortname

    @shortname.setter
    def shortname(self, value):
        self._shortname = value
        if self._hrn is None and self.authority:
            self.hrn = self.authority + value
        if self._id is None and self.hrn:
            self.id = hrn_to_urn(self.hrn, self._type)

    @property
    def hrn(self):
        return self._hrn

    @hrn.setter
    def hrn(self, value):
        self._hrn = value
        if self._id is None:
            self.id = hrn_to_urn(value, self._type)
        if self._authority is None:
            self.authority = '.'.join(value.split('.')[:-1])
        if self._shortname is None:
            self.shortname = value.split('.')[-1]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        if self._hrn is None:
            hrn,t = urn_to_hrn(value)
            self.hrn = hrn
        if self._authority is None:
            self.authority = '.'.join(self.hrn.split('.')[:-1])
        if self._shortname is None:
            self.shortname = self.hrn.split('.')[-1]

    def generate(self):
        if self.id:
            if self.hrn is None:
                hrn,t = urn_to_hrn(self.id)
                self.hrn = hrn
            if self.authority is None:
                self.authority = '.'.join(self.hrn.split('.')[:-1])
            if self.shortname is None:
                self.shortname = self.hrn.split('.')[-1]
        
   

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
