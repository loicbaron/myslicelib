from myslicelib import setup as s, Setup
from myslicelib.api import Api
from myslicelib.model import Entity, Entities
from myslicelib.query import Query

class ProjectQuery(Query):
    
    def __init__(self, entity: Entity, setup=None) -> None:
        super().__init__(entity, setup)

        if setup and isinstance(setup, Setup):
            _auth_setup = setup
        else:
            _auth_setup = s
        self.auth_api = getattr(Api(_auth_setup.endpoints, _auth_setup.credential), 'project')()

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
