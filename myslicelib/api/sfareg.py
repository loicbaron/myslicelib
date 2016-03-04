import traceback
from myslicelib.api.sfa import Api as SfaApi
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, Xrn

class SfaReg(SfaApi):

    def __init__(self, endpoint, credential):
        super(SfaReg, self).__init__(endpoint, credential)
        if os.path.isfile(credential.certificate):
            with open(credential.certificate, "r") as myfile:
                certificate = myfile.read()
        else:
            certificate = credential.certificate
        self.user_credential = self._proxy.GetSelfCredential(
                                        certificate,
                                        self.credential.hrn,
                                        'user')

    def _filter_records(self, type, result):
        filtered_records = []
        for record in result:
            if (record['type'] == type) or (type == "all"):
                filtered_records.append(record)
        return filtered_records

    def _list_entity(self, hrn=None):
        if hrn is None:
            hrn = self.version()['id']
        try:
            # attept to list the hrn first if it is an authority
            # if hrn is not an authority, it will list all elements
            return self._proxy.List(hrn, self.user_credential, {'recursive':True})
        except Exception as e:
            return self._proxy.List(self.version()['id'], self.user_credential, {'recursive':True})

    def _get_entity(self, hrn):
        if hrn:
            return self._proxy.Resolve(hrn, self.user_credential, {})
        return self._proxy.List(self.version()['id'], self.user_credential, {})

    def get(self, entity, urn=None):
        result = []
        try:
            hrn = None
            if urn is not None:
                xrn = Xrn(urn)
                obj_type = xrn.get_type()
                hrn = urn_to_hrn(urn, entity)
                if entity == obj_type:
                    return self._get_entity(hrn)
            results = self._list_entity(hrn)
            return self._filter_records(entity, results)
            
            #print(results)
            #for r in results:
            #    result.append(self._get_entity(r['hrn']))
            #else:
            #    result = self._get_entity(hrn)
        except Exception as e:
            traceback.print_exc()
            print(e)
            exit(1)

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
                    return self._proxy.GetCredential(self.user_credential, hrn, entity)
                else:
                    return self._proxy.GetCredential(self.user_credential, upper_hrn, entity)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
            return self.get_credential(upper_hrn, entity)

    def create(self, entity, urn, record_dict):
        try:
            hrn = urn_to_hrn(urn, entity)
            auth_cred = self.get_credential(hrn, 'authority')
            if auth_cred:
                record_dict["type"] = entity
                record_dict["hrn"] = hrn
                result = self._proxy.Register(record_dict, auth_cred)
                # XXX test the result either 1 or a gid
                return self.get(entity, urn)
            return []
        except Exception as e:
            traceback.print_exc()
            return []

    def delete(self, entity, urn):
        try:
            hrn = urn_to_hrn(urn, entity)
            auth_cred = self.get_credential(hrn, 'authority')
            if auth_cred:
                result = self._proxy.Remove(hrn, auth_cred, entity)
                if result == 1:
                    return True
                else:
                    raise Exception(result)
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    def update(self, entity, urn, record_dict):
        try:
            hrn = urn_to_hrn(urn, entity)
            if entity == 'user' and hrn == self.credential.hrn:
                cred = self.user_credential
            elif entity == 'slice':
                cred = self.get_credential(hrn, 'slice')
            else:
                cred = self.get_credential(hrn, 'authority')
            if cred:
                record_dict["type"] = entity
                record_dict["hrn"] = hrn
                result = self._proxy.Update(record_dict, cred)
                # XXX test the result either 1 or a gid
                return self.get(entity, urn)
            raise Exception("No Credential to update this", urn)
        except Exception as e:
            traceback.print_exc()
            return False

    # self.CreateGid
