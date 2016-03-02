from myslicelib.query import Query

class TestbedQuery(Query):

    def get(self, id=None):
        res = self.api.version()
        import pprint
        pprint.pprint(res)