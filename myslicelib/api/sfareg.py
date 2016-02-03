from myslicelib.api.sfa import Api as SfaApi

class SfaReg(SfaApi):
    def __init__():
        self.user_credential = self.GetSelfCredential(self.certificate, hrn, 'user')
        #{'user':'xxxx','authorities':{'onelab':'xxx','onelab.upmc'},'slices':{'slice_x':'xxx','slice_y':'xxx'}}
    
    def get(self, hrn, obj_type=None):
        try:
            result = self.Resolve(hrn, self.user_credential, {})
            #result = filter_records(obj_type, result)
        except Exception(e):
            return False
        return result
    
    def list(self, hrn=None, obj_type=None):
        try:
            if hrn is None:
                # Registry must advertise hrn in GetVersion
                # the hrn has to match the root authority
                hrn = self.version()['hrn']
            result = self.List(hrn, self.user_credential, {})
            #result = filter_records(obj_type, result)
        except Exception(e):
            return False
        return result
    
    def user(self, hrn):
        return self.get('user', hrn)
    
    def users(self, hrn=None):
        return self.list('user', hrn)

    def get_credential(self, hrn, obj_type):
        return self.GetCredential(self.user_credential, hrn, obj_type)

    # self.Register
    def create(self, record_dict, obj_type):
        auth_hrn = '.'.join(record_dict['hrn'].split('.')[:-1])
        auth_cred = self.get_credential(auth_hrn, 'authority')
        return self.Register(record_dict, auth_cred)

    def remove(self, hrn, auth_cred, obj_type):
        auth_hrn = '.'.join(record_dict['hrn'].split('.')[:-1])
        auth_cred = self.get_credential(auth_hrn, 'authority')
        return self.Remove(hrn, auth_cred, obj_type)

    # self.Update
    # self.Remove(hrn, auth_cred, obj_type)
    # self.CreateGid
