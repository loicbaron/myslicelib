from myslicelib import setup as s
from myslicelib.api import Api
from myslicelib.model import Entity, Entities
from myslicelib.query import Query

class ProjectQuery(Query):
    
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        self.auth_api = getattr(Api(s.endpoints, s.credential), 'project')()

    def update(self, params):
        if not self._id:
            raise Exception("No element specified")
        
        res = self.auth_api.update(self._id, params)
        c = self.collection(res['data'])
        c.logs = res['errors']
        return c

    def delete(self):
        if not self._id:
            raise Exception("No element specified")

        res = self.auth_api.delete(self._id)

        return res
