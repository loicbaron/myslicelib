from myslicelib.query import Query

class SliceQuery(Query):

    def get(self):
        res = self.api.get(self._id)
        result = {}
        for element in res:
            for k,v in element.items():
                if k in result:
                    # merge  
                    result[k] += v    
                else:
                    result[k] = v
        return self.collection([result])


    # def update(self, params):
    #     if not self._id:
    #         raise Exception("No element specified")

    #     res = self.api.update(self._id, params)
        
    #     
    #     pprint(result)

    #     #return self.collection(res)