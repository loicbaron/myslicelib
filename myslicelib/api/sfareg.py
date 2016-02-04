from myslicelib.api.sfa import Api as SfaApi


class SfaReg(SfaApi):
    def __init__(self, url, pkey, email=None, hrn=None, certfile=None, verbose=False, timeout=None):
        super(SfaReg, self).__init__(url, pkey, email, hrn, certfile, verbose, timeout)
        self.hrn = hrn
        with open (certfile, "r") as myfile:
            certificate = myfile.read()
        self.user_credential = self.GetSelfCredential(certificate, self.hrn, 'user')
         
        #{'user':'xxxx','authorities':{'onelab':'xxx','onelab.upmc'},'slices':{'slice_x':'xxx','slice_y':'xxx'}}
    
    def get(self, hrn, obj_type=None):
        try:
            result = self.Resolve(hrn, self.user_credential, {})
            #result = filter_records(obj_type, result)
        except Exception as e:
            import traceback
            traceback.print_exc()
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
        except Exception as e:
            return False
        return result
    
    def user(self, hrn):
        return self.get('user', hrn)
    
    def users(self, hrn=None):
        return self.list('user', hrn)

    def get_credential(self, hrn, obj_type):
        return self.GetCredential(self.user_credential, hrn, obj_type)

    # look up to see the upper has the credential
    def traceup_credential(self, hrn, obj_type):
        try:
            upper_hrn = '.'.join(hrn.split('.')[:-1])
            cred = self.get_credential(upper_hrn, obj_type)
            return cred
        except Exception as e:
            # go to upper level until reach the root level
            if upper_hrn:
                return self.traceup_credential(upper_hrn, obj_type)
            return False

    # (self.registery() in sfi)
    def create(self, record_dict, obj_type):
        try:
            auth_hrn = '.'.join(record_dict['hrn'].split('.')[:-1])
            auth_cred = self.traceup_credential(auth_hrn, 'authority')
            if auth_cred:
                record_dict["type"] = obj_type
                return self.Register(record_dict, auth_cred)
            return False
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False
    
    def delete(self, hrn, obj_type):
        try:
            auth_hrn = '.'.join(hrn.split('.')[:-1])
            auth_cred = self.traceup_credential(auth_hrn, 'authority')
            if auth_cred:
                return self.Remove(hrn, auth_cred, obj_type)
            return False
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    def update(self, record_dict, obj_type):
        try:
            if obj_type == 'user' and record_dict['hrn'] == self.hrn:
                cred = self.user_credential
            elif obj_type == 'slice':    
                # get credential of the slice object
                # if it doesn't succeed try to get an authority credential of an upper authority till the root
                cred = self.traceup_credential(record_dict['hrn'], obj_type)
            else:
                auth_hrn = '.'.join(record_dict['hrn'].split('.')[:-1])
                cred = self.traceup_credential(auth_hrn, 'authority')
            if cred:
                record_dict["type"] = obj_type
                return self.Update(record_dict, cred)
            return False
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    # self.CreateGid
