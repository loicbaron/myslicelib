import myslicelib

from copy import copy
from myslicelib.model import Entities, Entity
from myslicelib.query import q

from multiprocessing import Process, Queue

class Authorities(Entities):
    pass

# def worker(task_queue, done_queue):
#     while not task_queue.empty():
#         call = task_queue.get()
#         print(call)
#         result = call()
#         done_queue.put(result)

class Authority(Entity):
    _class = "Authority"
    _type = "authority"
    _collection ="Authorities"

    def __init__(self, data = {}):
        data = data if data is not None else {}
        data['pi_users'] = data.get('pi_users', [])
        data['users'] = data.get('users', [])
        data['slices'] = data.get('slices', [])
        super().__init__(data)

    def getUsers(self, attribute=False, pis = False):
        if attribute:
            if pis:
                return self.getAttribute('pi_users')
            else:
                return self.getAttribute('users')
        else:
            User = myslicelib.model.user.User
            result = []
            if pis:
                for urn in self.getAttribute('pi_users'):
                    result += q(User).id(urn).get()
            else:
                for urn in self.getAttribute('users'):
                    result += q(User).id(urn).get()
            return result

    def getPiUsers(self, attribute=False):
        if attribute:
            return self.getAttribute('pi_users')
        else:
            User = myslicelib.model.user.User
            result = []
            for urn in self.getAttribute('pi_users'):
                result += q(User).id(urn).get()
            return result

    def getSlices(self, attribute=False, setup=None):
        if attribute:
            return self.getAttribute('slices')
        else:
            from myslicelib.model.slice import Slice
            result = []
            for urn in self.getAttribute('slices'):
                result += q(Slice, setup=setup).id(urn).get()
            return result

    def addPi(self, user):
        self.appendAttribute('pi_users',user.id)
        return self

    def removePi(self, user):
        self.setAttribute('pi_users', list(set(self.getAttribute('pi_users')) - set([user.id])))
        return self

    def isPi(self, user):
        return user.id in self.getAttribute('pi_users')

    def delete(self, setup=None):
        User = myslicelib.model.user.User
        Project = myslicelib.model.project.Project

        for user in self.getAttribute('users'):
            User({"id":user}).delete()

        for proj in self.getAttribute('projects'):
            Project({"id":proj}).delete()

        if not self.id:
            raise Exception("No element specified")
        
        res = self._api(setup).delete(self.id)

        result = {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }

        return result
