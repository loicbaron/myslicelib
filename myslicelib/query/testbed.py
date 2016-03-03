from myslicelib.query import Query

class TestbedQuery(Query):

    def get(self):
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


