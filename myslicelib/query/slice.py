from myslicelib.query import Query
from myslicelib.util.checker import checker

class SliceQuery(Query):

    def _merge_dicts(self, res):
        result = {}
        for element in res:
            for k,v in element.items():
                if k in result:
                    # merge  
                    result[k] += v    
                else:
                    result[k] = v
        return [result]


    def get(self):
        res = self.api.get(self._id)
        #if self._filter:
        #    res = [x for x in res if checker(x, self._filter)]

        if self._id is None:
            return self.collection(res)
        
        return self.collection(self._merge_dicts(res))


    def update(self, params):
        if not self._id:
            raise Exception("No element specified")

        res = self.api.update(self._id, params)

        return self.collection(self._merge_dicts(res))
