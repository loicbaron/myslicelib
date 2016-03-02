import logging
from myslicelib import setup as s
from myslicelib.api import Api
from myslicelib.model import Entity

def q(entity: Entity):
    '''
    Factory function, used to build the correct QueryEntity object

    :param entity: object of class Entity
    :return: QueryEntity
    '''
    e = entity.__name__
    QueryModule = "myslicelib.query.{}".format(e.lower())
    QueryClass = e + "Query"
    print(QueryModule,QueryClass)
    try:
        module = __import__(QueryModule, fromlist=[QueryClass])
        return getattr(module, QueryClass)(entity)
    except ImportError:
        logging.error("Object {} not found".format(QueryClass))
        exit(1)


class Query(object):

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

        self.api = getattr(Api(s.endpoints, s.credential), self.entity.__name__.lower())()


        # self.api = Api(s.endpoints, s.credential)
        # self.api = self.api.resource()

        #for _e,_k in _entities:
        # res = self.api.version()
        #
        # for k in res['ams']:
        #     print("{} : ".format(k))
        #
        # m, c = entity.split('.')
        # model = 'myslicelib.model.%s' % m
        # try:
        #     module = __import__(model, fromlist=[c])
        # except ImportError:
        #     logging.error("Model %s not found" % m)
        #     exit(1)
        #
        # try:
        #     self.cls = getattr(module, c)
        # except AttributeError as e:
        #     logging.error(e)
        #     logging.error("%s entity not found" % (entity.__name__))
        #     exit(1)
        #
        #
        # self.api = Api(
        #             'https://www.planet-lab.eu/PLCAPI/',
        #             'password',
        #             'myops@planet-lab.eu',
        #             '1:l-a)be'
        # )
        #
        # self.e = entity
        # self.f = {}
        # self.r = None

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
    # def find(self):
    #     return self.execute()

    def id(self, id):
        self._id = id
        return self

    def get(self, id=None):
        res = self.api.get(id)
        for el in res:
            for prop in el:
                setattr(self.entity, prop, el[prop])
        return self.entity

    def update(self, id, params):
        res = self.api.update(id, params)
        import pprint
        pprint.pprint(res)

    def delete(self, id):
        res = self.api.delete(id)
        import pprint
        pprint.pprint(res)

