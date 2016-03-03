from myslicelib.query import Query
from myslicelib.error import MysNotSupportedError

class TestbedQuery(Query):

    def get(self):
        '''
        Testbed information are taken using the version() call

        :return:
        '''
        testbeds = []

        result = self.api.version()
        for el in result['ams']:
            import pprint
            pprint.pprint(el)
            testbeds.append(el)


        return self.collection(testbeds)

    def update(self):
        raise MysNotSupportedError("This function is not supported")

    def delete(self):
        raise MysNotSupportedError("This function is not supported")
