from myslicelib.query import Query
from myslicelib.model.testbed import Testbed, Testbeds

class TestbedQuery(Query):

    def get(self):
        res = self.api.version()


