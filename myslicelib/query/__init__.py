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
    try:
        module = __import__(QueryModule, fromlist=[QueryClass])
        return getattr(module, QueryClass)(entity)
    except ImportError:
        logging.error("Object {} not found".format(QueryClass))
        exit(1)


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

        self.api = getattr(Api(s.endpoints, s.credential), self.entity.__name__.lower())()


    def id(self, id):
        self._id = id
        return self

    def get(self):
        res = self.api.get(self._id)
        for el in res:
            for prop in el:
                setattr(self.entity, prop, el[prop])
        return self.entity

    def update(self, params):
        if not self._id:
            raise Exception("No element specified")
        res = self.api.update(id, params)
        import pprint
        pprint.pprint(res)

    def delete(self):
        if not self._id:
            raise Exception("No element specified")
        res = self.api.delete(id)
        import pprint
        pprint.pprint(res)

