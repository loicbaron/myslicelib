import threading

class ThreadHandler(threading.Thread):

    def __init__(self, target=None, args=(), kwargs=None,):
        super(ThreadHandler, self).__init__(target=target)
        self.args = args
        self.kwargs = kwargs