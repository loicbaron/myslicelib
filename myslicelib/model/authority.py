from myslicelib.model import Entities, Entity
from myslicelib.model.user import Users, User
from myslicelib.query import q

class Authorities(Entities):
    pass

class Authority(Entity):
    _name = "Authority"

    @property
    def users(self):
        pass

    @property
    def projects(self):
        pass

    def pis(self, id=None):
        users = Users()
        for pi in self.pis:
            urn = hrn_to_urn(pi)
            users.append(q(User).get(urn))
        return users

