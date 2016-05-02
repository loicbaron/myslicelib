import logging
from myslicelib import setup as s, Setup
from myslicelib.api import Api
from myslicelib.model import Entity, Entities
from myslicelib.util.checker import checker
from collections import defaultdict

def q(entity: Entity, setup=None):
    '''
    Factory function, used to build the correct QueryEntity object

    :param entity: object of class Entity
    :return: QueryEntity
    '''
    e = entity._class
    QueryModule = "myslicelib.query.{}".format(e.lower())
    QueryClass = e + "Query"
    try:
        module = __import__(QueryModule, fromlist=[QueryClass])
        return getattr(module, QueryClass)(entity, setup)
    except ImportError:
        logging.error("Class {} not found".format(QueryClass))
        exit(1)

class Query(object):

    _id = None

    def __init__(self, entity: Entity, setup=None) -> None:

        if setup and isinstance(setup, Setup):
            self._setup = setup
        else:
            self._setup = s

        self.entity = entity
        self._filter = defaultdict(set)
        self.api = getattr(Api(self._setup.endpoints, self._setup.authentication), self.entity._type)()

    def collection(self, elements=None):
        '''
        Returns the instantiated collection class corresponding to secified Entity,
        or Entities if it is not defined

        if elements is defined (must be a list of dictionaries) will populate the collection

        :return:
        '''
        # the default collection
        collection = Entities()
        try:
            CollectionClass = self.entity._collection
        except AttributeError:
            logging.error("Class {} not found, using default Entities".format(CollectionClass))
        finally:
            try:
                CollectionModule = "myslicelib.model.{}".format(self.entity._class.lower())
                module = __import__(CollectionModule, fromlist=[CollectionClass])
                collection = getattr(module, CollectionClass)()
            except ImportError:
                logging.error("Class {} not found, using default Entities".format(CollectionClass))
        if (elements):
            for el in elements:
                collection.add(self.entity(el))
        return collection

    def id(self, id):
        self._id = id
        return self

    def get(self):
        res = self.api.get(self._id)
        
        if self._filter:
            res['data'] = [x for x in res['data'] if checker(x, self._filter)]

        # c is Entities object
        c = self.collection(res['data']) 
        c.logs = res['errors']
        return c

    def update(self, params):
        if not self._id:
            raise Exception("No element specified")
        res = self.api.update(self._id, params)
        c = self.collection(res['data'])
        c.logs = res['errors']
        return c

    def delete(self):
        if not self._id:
            raise Exception("No element specified")

        res = self.api.delete(self._id)
        return res 

    def filter(self, key, value, option='equal'):
        # if option == 'equal':
        #     self._filter.append({
        #                     'key': key,
        #                     'value': value,
        #                    })
        # if option == 'in':
        #     for el in value:
        #         if key in self._filter:
        #             self._filter += []
        if isinstance(value, str):
            self._filter[key].update(set([value]))
        else:
            self._filter[key].update(set(value))
        #print(self._filter)
        return self
