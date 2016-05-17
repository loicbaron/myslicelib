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

    def __init__(self, data= {}):
        super().__init__(data)
        self.pi_users = data.get('pi_users', [])
        self.slices = data.get('slices', [])

    def getUsers(self, pis = False):
        User = myslicelib.model.user.User
        result = []
        if pis:
            for urn in self.attribute('pi_users'):
                result += q(User).id(urn).get()
        else:
            for urn in self.attribute('users'):
                result += q(User).id(urn).get()
        return result

    def getPiUsers(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('pi_users'):
            result += q(User).id(urn).get()
        return result

    def getSlices(self):
        from myslicelib.model.slice import Slice
        result = []
        for urn in self.attribute('slices'):
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

        self._api = self._setup_api(setup)

        if not self.id:
            raise Exception("No element specified")
        
        for user in self.users:
            self._api.delete(user)

        for sli in self.slices:
            self._api.delete(sli)

        for proj in self.projects:
            self._api.delete(proj)
            
        res = self._api.delete(self.id)

        result = {
                'data': res.get('data', []),
                'errors': res.get('errors', []),
        }

        return result