from myslicelib.query import Query
from myslicelib.error import MysNotSupportedError
from myslicelib.util.checker import checker

from pprint import pprint

class TestbedQuery(Query):

    def get(self):
        '''
        Testbed information are taken using the version() call

        :return:
        '''
        testbeds = []

        res = self.api.version()

        if self._filter:
            res['data'] = [x for x in res['data'] if checker(x, self._filter)]

        # c is Entities object
        c = self.collection(res['data']) 
        c.logs = res['errors']
        return c


    def update(self):
        raise MysNotSupportedError("This function is not supported")

    def delete(self):
        raise MysNotSupportedError("This function is not supported")
