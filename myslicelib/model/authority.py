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
        super().__init__(data)
        if data is None:
            data = {}
        self.pi_users = data.get('pi_users', [])
        self.slices = data.get('slices', [])

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

    def getPiUsers(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.getAttribute('pi_users'):
            result += q(User).id(urn).get()
        return result

    def getSlices(self, attribute=False):
        if attribute:
            return self.getAttribute('slices')
        else:
            from myslicelib.model.slice import Slice
            result = []
            for urn in self.getAttribute('slices'):
                result += q(Slice).id(urn).get()
            return result

    def addPi(self, user):
        self.pi_users.append(user.id)
        return self

    def removePi(self, user):
        self.pi_users = list(set(self.pi_users) - set(user.id))
        return self

    def isPi(self, user):
        return user.id in self.pi_users

    def delete(self, setup=None):
        User = myslicelib.model.user.User
        Project = myslicelib.model.project.Project

        for user in self.users:
            User({"id":user}).delete()

        for proj in self.projects:
            Project({"id":proj}).delete()

        if not self.id:
            raise Exception("No element specified")
        
        self._api = self._setup_api(setup)

        res = self._api.delete(self.id)

        result = {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }

        return result
