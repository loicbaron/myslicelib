import myslicelib
from pprint import pprint

from myslicelib.model.user import User
from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q

class Projects(Authorities):
    pass

class Project(Authority):
    _class = "Project"
    # XXX TBD either use class name lower or use type???
    _type = "project"
    _collection = "Projects"

    def save(self, setup=None):

        # Adding/Removing Users to/from the slices when project.save()
        sl = self.getSlices()
        for s in sl:
            adding = list(set(self.getAttribute('pi_users')) - set(s.getAttribute('users')))
            deleting = list(set(s.getAttribute('users')) - set(self.getAttribute('pi_users')))
            for u in adding:
                user = q(User).id(u).get().first()
                s.addUser(user)
            for u in deleting:
                user = q(User).id(u).get().first()
                print(user)
                s.removeUser(user)
            s.save(setup)

        return super().save(setup)

    def getUsers(self, attribute=False, pis = True):
        return super(Project, self).getUsers(attribute, pis)

    def getAuthority(self, attribute=False):
        if attribute:
            return self.getAttribute('authority')
        else:
            auth_id = self.id.replace(':'+self.id.split('+')[1].split(':')[-1],'')
            return q(Authority).id(auth_id).get().first()

    def addPi(self, user):
        self.appendAttribute('pi_users', user.id)
        return self

    def removePi(self, user):
        self.setAttribute('pi_users', list(set(self.getAttribute('pi_users')) - set([user.id])))
        return self

    def delete(self, setup=None):
        Slice = myslicelib.model.slice.Slice

        for sli in self.slices:
            Slice({"id": sli}).delete()

        if not self.id:
            raise Exception("No element specified")
            
        res = self._api(setup).delete(self.id)

        result = {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }

        return result
