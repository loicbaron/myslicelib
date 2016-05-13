import myslicelib

from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q

class Projects(Authorities):
    pass

class Project(Authority):
    _class = "Project"
    # XXX TBD either use class name lower or use type???
    _type = "project"
    _collection = "Projects"

    def getAuthority(self):
        auth_id = self.id.replace(':'+self.id.split('+')[1].split(':')[-1],'')
        return q(Authority).id(auth_id).get().first()

    def addPi(self, user):
        self.pi_users.append(user.id)
        sl = self.getSlices()
        for s in sl:
            s.addUser(user)
        return self

    def removePi(self, user):
        self.pi_users = set(self.pi_users) - set([user.id])
        sl = self.getSlices()
        for s in sl:
            s.removeUser(user)
        return self

