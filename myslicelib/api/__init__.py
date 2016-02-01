'''
Base API Class
'''


class Api(object):

    def __init__(self):
        pass

    def version(self):
        raise NotImplementedError('Not implemented')

    def get(self):
        raise NotImplementedError('Not implemented')

    def update(self):
        raise NotImplementedError('Not implemented')

    def delete(self):
        raise NotImplementedError('Not implemented')