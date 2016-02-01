from myslicelib.api.sfa import Api as SfaApi

class SfaReg(SfaApi):

    def version():
        try:
            result = self.GetVersion()
        except Exception, e:
            return False
        return result

    def get(obj_type, hrn):
        try:
            result = self.Resolve(hrn, self.credential, {})
            #result = filter_records(obj_type, result)
        except Exception, e:
            return False
        return result

    def user(hrn):
        return self.get('user', hrn)

