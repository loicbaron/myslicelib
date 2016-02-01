from myslicelib.query import Query

class UserQuery(Query):

    def all(self):
        self.api.users().get()
