from myslicelib.query import Query
from myslicelib.util.checker import checker

class SliceQuery(Query):

    def _merge_dicts(self, res):
        result = {}
        # element could be slice from reg
        # could be resources from am, leases from am
        for element in res:
            for key, value in element.items():
                if key in result:
                    # append
                    result[key] += value    
                else:
                    result[key] = value
        return [result]


    def get(self):
        res = self.api.get(self._id)
        if self._filter:
            res = [x for x in res if checker(x, self._filter)]

        if self._id:
            return self.collection(self._merge_dicts(res))

        return self.collection(res)

    def update(self, params):
        if not self._id:
            raise Exception("No element specified")

        res = self.api.update(self._id, params)

        return self.collection(self._merge_dicts(res))
