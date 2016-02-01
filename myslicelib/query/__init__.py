from myslicelib.api.planetlab import Api
from myslicelib.model import Entities
import logging

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

    def __init__(self, entity):
        '''
        dynamically loads the module and instantiate the class
        self.cls will be the class to be used to populate the objects
        '''
        m, c = entity.split('.')
        model = 'myslicelib.model.%s' % m
        try:
            module = __import__(model, fromlist=[c])
        except ImportError:
            logging.error("Model %s not found" % m)
            exit(1)

        try:
            self.cls = getattr(module, c)
        except AttributeError as e:
            print e
            print "%s entity not found" % (entity.__name__)
            exit(1)


        self.api = Api(
                    'https://www.planet-lab.eu/PLCAPI/',
                    'password',
                    'myops@planet-lab.eu',
                    '1:l-a)be'
        )

        self.e = entity
        self.f = {}
        self.r = None


   
    def filter(self, key, value):
        self.f[key] = value
        return self
    
    def order(self, order):
        return self.sort(order)

    def sort(self, sort):
        return self.filter('-SORT', sort)
    
    def offset(self, offset):
        if offset > 0:
            return self.filter('-OFFSET', offset)
        return self
        
    def limit(self, limit):
        return self.filter('-LIMIT', limit)
    
    def gt(self, key, value):
        return self.filter('>' + key, value)
    
    def gte(self, key, value):
        return self.filter(']' + key, value)
    
    def lt(self, key, value):
        return self.filter('<' + key, value)
    
    def lte(self, key, value):
        return self.filter('[' + key, value)

    def find(self):
        return self.execute()
    
    def execute(self):

        es = Entities()
        for el in self.api.get(self.cls.__name__):
            es.add(self.cls(el))
        return es

        es = []
        for el in self.api.select(self.cls.__name__, self.f, self.r):
            es.add(self.cls(el))
        return es