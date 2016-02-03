from myslicelib.api.sfa import Api as SfaApi

class SfaAm(SfaApi):

    def get(self, obj_type, hrn):
        try:
            api_options = {}
            if obj_type == 'resource':
                result = self.ListResources([self.user_credential], api_options)
                # filter and return the resource
            elif obj_type == 'slice':
                result = self.Describe([urn], self.slice_credential, api_options)
            else:
                raise NotImplementedError('Not implemented')
        except Exception, e:
            return False
        return result
    
    def list(self, obj_type, hrn=None):
        try:
            api_options = {'rspec_type': 'GENI', 'rspec_version': '3'}
            if hrn is None:
                result = self.ListResources([self.user_credential], api_options)
            else:
                if self.version()['geni_api']==3:
                    result = self.Describe([urn], self.slice_credential, api_options)
                elif self.version()['geni_api']==2:
                    api_options['geni_slice_urn'] = hrn_to_urn(hrn, 'slice')
                    result = self.ListResources([urn], self.slice_credential, api_options)
                else:
                    raise NotImplementedError('Not implemented')
        except Exception, e:
            return False
        return result


        # self.Status
        # self.CreateSliver (v2)
        # self.Allocate
        # self.Provision
        # self.PerformOperationalAction
        # self.Renew
        # self.Shutdown
        # self.Delete
