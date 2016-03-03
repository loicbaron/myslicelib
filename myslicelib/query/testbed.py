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
            testbeds.append(
                {
                    'id': el['version']['id'],
                    'name': el['name'],
                    'api': el['protocol'],
                    'api_version': el['version']['version'],
                    'api_url': el['url'],
                    'api_backend': el['version']['backend'],
                }
            )

        return self.collection(testbeds)

    def update(self):
        raise MysNotSupportedError("This function is not supported")

    def delete(self):
        raise MysNotSupportedError("This function is not supported")
