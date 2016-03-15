from myslicelib import setup as s
from myslicelib.api import Api
from myslicelib.model import Entity, Entities
from myslicelib.query import Query

class ProjectQuery(Query):
    
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.api = getattr(Api(s.endpoints, s.credential), 'project')()
        self.auth_api = getattr(Api(s.endpoints, s.credential), 'authority')()

    def get(self):
        res = self.api.get(self._id)
        return self.collection(res)

    def update(self, params):

        if not self._id:
            raise Exception("No element specified")

        res = self.auth_api.update(self._id, params)

        return self.collection(res)

    def delete(self):
        if not self._id:
            raise Exception("No element specified")

        res = self.auth_api.delete(self._id)

        return res 
