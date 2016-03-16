import myslicelib

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

    @property
    def users(self):
        User = myslicelib.model.user.User
        result = []
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

    @users.setter
    def users(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.setattribute('users', value)

    @property
    def pi_users(self):
        User = myslicelib.model.user.User
        result = []
        for urn in self.attribute('pi_users'):
            result += q(User).id(urn).get()
        return result

    @pi_users.setter
    def pi_users(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.setattribute('pi_users', value)

    @property
    def slices(self):
        Slice = myslicelib.model.slice.Slice
        result = []
        for urn in self.attribute('slices'):
            result += q(Slice).id(urn).get()
        return result

    @slices.setter
    def slices(self, value):
        if not isinstance(value, list):
            raise TypeError('a list needed to set')
        self.setattribute('slices', value)
        # TOD0: SFAAM UPDATE
