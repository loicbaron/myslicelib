import traceback
from myslicelib.api.sfa import Api as SfaApi


class SfaReg(SfaApi):

    def __init__(self, endpoint, credential):
        super(SfaReg, self).__init__(endpoint, credential)
        with open(self.credential.certificate, "r") as myfile:
            certificate = myfile.read()
        self.user_credential = self.proxy.GetSelfCredential(
                                        certificate,
                                        self.credential.hrn,
                                        'user')

    def get(self, hrn, obj_type=None):
        try:
            result = self.proxy.Resolve(hrn, self.user_credential, {})
            # result = filter_records(obj_type, result)
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def list(self, hrn=None, obj_type=None):
        try:
            if hrn is None:
                # Registry must advertise hrn in GetVersion
                # the hrn has to match the root authority
                hrn = self.version()['hrn']
            result = self.proxy.List(hrn, self.user_credential, {})
            # result = filter_records(obj_type, result)
        except Exception as e:
            return False
        return result

    def user(self, hrn):
        return self.get(hrn, 'user')

    def users(self, hrn=None):
        return self.list(hrn, 'user')

    # look up to see the upper has the credential
    def get_credential(self, hrn, obj_type):
        try:
            upper_hrn = '.'.join(hrn.split('.')[:-1])
            if upper_hrn:
                if obj_type == 'slice':
                    return self.proxy.GetCredential(self.user_credential, hrn, obj_type)
                else:
                    return self.proxy.GetCredential(self.user_credential, upper_hrn, obj_type)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
            return self.get_credential(upper_hrn, obj_type)

    def create(self, record_dict, obj_type):
        try:
            auth_cred = self.get_credential(record_dict['hrn'], 'authority')
            if auth_cred:
                record_dict["type"] = obj_type
                return self.proxy.Register(record_dict, auth_cred)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    def delete(self, hrn, obj_type):
        try:
            auth_cred = self.get_credential(hrn, 'authority')
            if auth_cred:
                return self.proxy.Remove(hrn, auth_cred, obj_type)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    def update(self, record_dict, obj_type):
        try:
            if obj_type == 'user' and record_dict['hrn'] == self.credential.hrn:
                cred = self.user_credential
            elif obj_type == 'slice':
                cred = self.get_credential(record_dict['hrn'], 'slice')
            else:
                cred = self.get_credential(record_dict['hrn'], 'authority')
            if cred:
                record_dict["type"] = obj_type
                return self.proxy.Update(record_dict, cred)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    @staticmethod
    def filter_records(type, records):
        filtered_records = []
        for record in records:
            if (record['type'] == type) or (type == "all"):
                filtered_records.append(record)
        return filtered_records


    # self.CreateGid