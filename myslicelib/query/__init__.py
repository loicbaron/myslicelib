import logging
from myslicelib import setup as s
from myslicelib.api import Api
from myslicelib.model import Entity, Entities

def q(entity: Entity):
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
        return getattr(module, QueryClass)(entity)
    except ImportError:
        logging.error("Class {} not found".format(QueryClass))
        exit(1)

def checker(dict_in, dict_filter):
    global flag
    flag = False
    
    def extract(dict_in, dict_filter):
        global flag
        for key, value in dict_in.items():
            if not flag:
                if isinstance(value, dict): # If value itself is dictionary
                    extract(value, dict_filter)
                elif isinstance(value, list):
                    for el in value:
                        if isinstance(el, str):
                            # XXX We only support == operator at the moment 
                            if key == dict_filter['key'] and el == dict_filter['value']:
                                flag = True
                                break
                        else:
                            extract(el, dict_filter)
                elif isinstance(value, str):
                    # XXX We only support == operator at the moment 
                    if key == dict_filter['key'] and value == dict_filter['value']:
                        flag = True
                        break

    extract(dict_in, dict_filter)
    return flag

class Query(object):

    _id = None

    # def __new__(cls, *args, **kwargs):
        # if cls is Query:
        #     try :
        #         __import__(args[0])
        #         return super(Query, cls).__new__(type(args[0].capitalize(), (), {}))
        #     except ImportError :
        #         logging.error("Entity %s not found" % (args[0]))
        #         exit(1)


        #
        # if cls is Query:
        #     print subcls
        #     for x in cls.__subclasses__():
        #         if x.__name__ == subcls:
        #             return super(Query, cls).__new__(x)
        # else:
        #     return super(Query, cls).__new__(cls, *args, **kwargs)

    def __init__(self, entity: Entity) -> None:

        self.entity = entity
        self._filter = []
        self.api = getattr(Api(s.endpoints, s.credential), self.entity._type)()

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

    #collections is no longer a 
    def get(self):
        res = self.api.get(self._id)
        if self._filter:
            for f in self._filter:
                res = [x for x in res if checker(x, f)]
        return self.collection(res)


    def update(self, params):
        if not self._id:
            raise Exception("No element specified")

        res = self.api.update(self._id, params)
        return self.collection(res)

    def delete(self):
        if not self._id:
            raise Exception("No element specified")

        res = self.api.delete(self._id)
        return res 

    def filter(self, key, value, op = '='):
        self._filter.append({
                        'key':key,
                        'value':value,
                        'op':op
                       })
        return self

