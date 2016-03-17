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

class Projects(Entities):
    pass

class Authority(Entity):
    _class = "Authority"
    _type = "authority"
    _collection ="Authorities"

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
        # task_queue = Queue()
        # done_queue = Queue()
        # for urn in self.attribute('users'):
        #     task_queue.put(lambda x: x+1)

        # for i in range(3):
        #     p = Process(target=worker, args=(task_queue, done_queue))
        #     print('doing')
        #     p.start()

        # for i in range(3):
        #     p.join()

        # done_queue.join()

        # result = []
        # while not done_queue.empty():
        #     result += done_queue.get()

        # return result

    def getSlices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attribute('slices'):
            result += q(Slice).id(urn).get()
        return result

    def addPi(self, user):
        self.pi_users.append(user.id)
        return self

    def removePi(self, user):
        self.pi_users = set(self.pi_users) - set(user.id)
        return self

    def getPi_users(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('pi_users'):
            result += q(User).id(urn).get()
        return result
