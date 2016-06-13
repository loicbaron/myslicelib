from myslicelib import setup as s, Setup
from myslicelib.api import Api
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn

class Entity(object):
    _type = 'entity'

    def __init__(self, data = {}):
        # prevents infinite recursion from self._attributes = {}
        # as now we have __setattr__, which will call __getattr__ when the line
        # self._attributes[k] tries to access self.data, won't find it in the instance
        # dictionary and return self._attributes[k] will in turn call __getattr__
        # for the same reason and so on.... so we manually set _attributes initially
        super().__setattr__('_attributes', data)

    def __repr__(self):
        return "%s" % (self.getAttributes())

    def __getattr__(self, name):
        # we avoid recursion
        if name.startswith('get'):
            raise AttributeError

        try:
            ##
            # Check if a getter function is defined
            camelName = ''.join(x for x in name.replace('_',' ').title() if not x.isspace())
            return getattr(self, 'get' + camelName)(True)
        except:
            return self.getAttribute(name)

    def __setattr__(self, name, value):
        # we avoid recursion
        if name.startswith('set'):
            raise AttributeError

        try:
            camelName = ''.join(x for x in name.replace('_',' ').title() if not x.isspace())
            getattr(self, 'set' + camelName)(value)
        except:
            #import traceback
            #traceback.print_exc()
            self.setAttribute(name, value)

    def hasAttribute(self, name):
        try:
            return self._attributes[name]
        except KeyError:
            return False

    def getAttributes(self):
        return self._attributes

    def getAttribute(self, name):
        try:
            return self._attributes[name]
        except KeyError :
            raise AttributeError('Entity object has no attribute %s' % name)

    ##
    # ID (URN)
    def getId(self):
        if not self.hasAttribute('id') and self.hrn:
            self.setAttribute('id', hrn_to_urn(self.hrn, self._type))

        return self.getAttribute('id')

    def setId(self, value):
        self.setAttribute('id', value)
        hrn = urn_to_hrn(value)[0]
        self.setAttribute('hrn', hrn)
        auth = hrn_to_urn('.'.join(hrn.split('.')[:-1]), 'authority')
        self.setAttribute('authority', auth)
        self.setAttribute('shortname', hrn.split('.')[-1])

    ##
    # HRN
    def getHrn(self):
        if not self.hasAttribute('hrn') and self.hasAttribute('id'):
            self.setAttribute('hrn', urn_to_hrn(self.id)[0])

        return self.getAttribute('hrn')

    def setHrn(self, value):
        self.setAttribute('hrn', value)
        self.setAttribute('id', hrn_to_urn(value, self._type))
        auth = hrn_to_urn('.'.join(value.split('.')[:-1]), 'authority')
        self.setAttribute('authority', auth)
        self.setAttribute('shortname', value.split('.')[-1])

    ##
    # SHORTNAME
    def getShortname(self):
        if not self.hasAttribute('shortname'):
            self.setAttribute('shortname', self.hrn.split('.')[-1])

        return self.getAttribute('shortname')

    def setShortname(self, value):
        self.setAttribute('shortname', value)
        if 'authority' in self._attributes:
            auth_hrn = urn_to_hrn(self.authority)[0]
            hrn = auth_hrn + '.' + value
            self.setAttribute('hrn', hrn)
            self.setAttribute('id', hrn_to_urn(hrn, self._type))

    def setAuthority(self, value):
        self.setAttribute('authority', value)
        if 'shortname' in self._attributes:
            hrn = value + '.' + self.shortname
            self.setAttribute('hrn', hrn)
            self.setAttribute('id', hrn_to_urn(hrn, self._type))

    def setAttribute(self, name, value):
        self._attributes[name] = value

    def dict(self):
        return self._attributes

    def clear(self):
        self.attribute = {}

    def _api(self, setup):
        if setup and isinstance(setup, Setup):
            _setup = setup
        else:
            _setup = s

        # using _type instead of _class as project is an authority in SFA Reg
        return getattr(Api(_setup.endpoints, _setup.authentication), self._type)()

    def save(self, setup=None):
        # the following will trigger the automatic eneration of the id, hrn and
        # shortname if they don't exist
        if not self.id:
            pass

        if not self.hrn:
            pass

        if not self.shortname:
            pass

        res = self._api(setup).update(self.id, self.getAttributes())

        return {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }

    def delete(self, setup=None):

        if not self.id:
            raise Exception("No element specified")

        res = self._api(setup).delete(self.id)
        
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
        for el in self:
            list.append(el.getAttributes())

        return list

    def save(self):
        for el in self:
            el.save()

    def delete(self):
        for el in self:
            el.delete()

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
