from myslicelib.query import Query
from myslicelib.model.testbed import Testbed, Testbeds

class TestbedQuery(Query):

    def get(self):
        testbeds = Testbeds()

        result = self.api.version()
        for el in result['ams']:
            testbed = self.entity()
            testbed.id = el['version']['id']
            testbed.name = el['name']
            testbed.api = el['protocol']
            testbed.api_version = el['version']['version']
            testbed.api_url = el['url']
            testbed.api_backend = el['version']['backend']
            testbeds.add(testbed)

        return testbeds


