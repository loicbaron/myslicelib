import traceback
from myslicelib.api.sfa import Api as SfaApi
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn


class SfaReg(SfaApi):

    def __init__(self, endpoint, credential):
        super(SfaReg, self).__init__(endpoint, credential)
        with open(self.credential.certificate, "r") as myfile:
            certificate = myfile.read()
        self.user_credential = self.proxy.GetSelfCredential(
                                        certificate,
                                        self.credential.hrn,
                                        'user')

    def _filter_records(type, result):
        filtered_records = []
        for record in result:
            if (record['type'] == type) or (type == "all"):
                filtered_records.append(record)
        return filtered_records

    def _list_entity(self, hrn):
        try:
            # attept to list the hrn first if it is an authority
            # if hrn is not an authority, it will list all elements
            return self.proxy.List(hrn, self.user_credential, {})
        except Exception as e:
            return self.proxy.List(self.version()['hrn'], self.user_credential, {})

    def _get_entity(self, hrn):
        if hrn:
            return self.proxy.Resolve(hrn, self.user_credential, {})
        return self.proxy.List(self.version()['hrn'], self.user_credential, {})

    def get(self, entity, urn=None):
        result = []
        try:
            obj_type = None
            if urn is not None:
                hrn, obj_type = urn_to_hrn(urn, entity)
            if urn is None or obj_type == 'authority':
                results = self._list_entity(hrn)
                results = self._filter_records(entity, results)
                for r in results:
                    result.append(self._get_entity(r['hrn']))
            else:
                result = self._get_entity(hrn)
        except Exception as e:
            print(e)
            exit(1)
        
        if raw or not entity:
            return result

        # only authority can list enities
        #result = self._filter_records(entity, result)
        return result

    # def get(self, hrn, entity=None):
    #     try:
    #         
    #         # result = filter_records(entity, result)
    #     except Exception as e:
    #         traceback.print_exc()
    #         return False
    #     return result

    # look up to see the upper has the credential
    def get_credential(self, hrn, entity):
        try:
            upper_hrn = '.'.join(hrn.split('.')[:-1])
            if upper_hrn:
                if entity == 'slice':
                    return self.proxy.GetCredential(self.user_credential, hrn, entity)
                else:
                    return self.proxy.GetCredential(self.user_credential, upper_hrn, entity)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
            return self.get_credential(upper_hrn, entity)

    def create(self, record_dict, entity):
        try:
            auth_cred = self.get_credential(record_dict['hrn'], 'authority')
            if auth_cred:
                record_dict["type"] = entity
                return self.proxy.Register(record_dict, auth_cred)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    def delete(self, hrn, entity):
        try:
            auth_cred = self.get_credential(hrn, 'authority')
            if auth_cred:
                return self.proxy.Remove(hrn, auth_cred, entity)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    def update(self, record_dict, entity):
        try:
            if entity == 'user' and record_dict['hrn'] == self.credential.hrn:
                cred = self.user_credential
            elif entity == 'slice':
                cred = self.get_credential(record_dict['hrn'], 'slice')
            else:
                cred = self.get_credential(record_dict['hrn'], 'authority')
            if cred:
                record_dict["type"] = entity
                return self.proxy.Update(record_dict, cred)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    # self.CreateGid
