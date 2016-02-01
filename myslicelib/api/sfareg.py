from myslicelib.api.sfa import Api as SfaApi

class SfaReg(SfaApi):


     def get(self, obj_type, hrn):
         try:
             result = self.Resolve(hrn, self.credential, {})
             #result = filter_records(obj_type, result)
         except Exception, e:
             return False
         return result

     def list(self, obj_type, hrn=None):
         try:
             if hrn is None:
                 # Registry must advertise hrn in GetVersion
                 # the hrn has to match the root authority
                 hrn = self.version['hrn']
             result = self.List(hrn, self.credential, {})
             #result = filter_records(obj_type, result)
         except Exception, e:
             return False
         return result

     def user(self, hrn):
         return self.get('user', hrn)

     def users(self, hrn=None):
         return self.list('user', hrn)

