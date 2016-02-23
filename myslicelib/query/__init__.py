from myslicelib import setup as s
from myslicelib.api import Api
from myslicelib.model import Entities

class Query(object):

    _entities = {
        'Resources' : 'resource'
    }

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

    def __init__(self, entities: Entities) -> None:

        if not entities.__name__ in self._entities:
            raise NotImplementedError("Invalid object {} or not implemented".format(entities.__name__))

        self.entities = entities


        self.api = getattr(Api(s.endpoints, s.credential), self._entities[entities.__name__])()

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



    def get(self):

        res = self.api.get()

        print(res)