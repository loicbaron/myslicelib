import myslicelib

from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q

class Projects(Authorities):
    pass

class Project(Authority):
    _class = "Project"
    _type = "authority"
    _collection = "Projects"

    def getAuthority(self):
        auth_id = self.id.replace(':'+self.id.split('+')[1].split(':')[-1],'')
        return q(Authority).id(auth_id).get().first()
