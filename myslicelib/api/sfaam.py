import xmltodict
from myslicelib.api.sfa import Api as SfaApi

def hrn_to_urn(hrn,type): return Xrn(hrn, type=type).urn

# self.ListResources
# self.Status   => geni_urn + geni_slivers
# self.Describe => geni_urn + geni_slivers + geni_rspec
# self.CreateSliver (v2)
# self.Allocate
# self.Provision
# self.PerformOperationalAction
# self.Renew
# self.Shutdown
# self.Delete

class SfaAm(SfaApi):

    def get(self, obj_type, hrn):
        try:
            api_options = {}
            if obj_type == 'resource':
                result = self.ListResources([self.user_credential], api_options)
                # filter and return the resource
            elif obj_type == 'slice':
                if version['geni_api'] == 2:
                    api_options['geni_slice_urn'] = hrn_to_urn(hrn)
                    result = server.ListResources([object_cred], api_options)

                result = self.Describe([urn], self.slice_credential, api_options)
            else:
                raise NotImplementedError('Not implemented')

            dict_result = xmltodict.parse(result['value'])
            result['parsed'] = dict_result

        except Exception as e:
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
        except Exception as e:
            return False
        return result

class Xrn:

    ########## basic tools on HRNs
    # split a HRN-like string into pieces
    # this is like split('.') except for escaped (backslashed) dots
    # e.g. hrn_split ('a\.b.c.d') -> [ 'a\.b','c','d']
    @staticmethod
    def hrn_split(hrn):
        return [ x.replace('--sep--','\\.') for x in hrn.replace('\\.','--sep--').split('.') ]

    # e.g. hrn_auth_list ('a\.b.c.d') -> ['a\.b', 'c']
    @staticmethod
    def hrn_auth_list(hrn): return Xrn.hrn_split(hrn)[0:-1]

    def __init__ (self, xrn="", type=None, id=None):
        if not xrn: xrn = ""
        # user has specified xrn : guess if urn or hrn
        self.id = id
        if Xrn.is_urn(xrn):
            self.hrn=None
            self.urn=xrn
            if id:
                self.urn = "%s:%s" % (self.urn, str(id))
            self.urn_to_hrn()
        else:
            self.urn=None
            self.hrn=xrn
            self.type=type
            self.hrn_to_urn()
        self._normalize()

    def _normalize(self):
        if self.hrn is None: raise(SfaAPIError, "Xrn._normalize")
        if not hasattr(self,'leaf'): 
            self.leaf=Xrn.hrn_split(self.hrn)[-1]
        # self.authority keeps a list
        if not hasattr(self,'authority'): 
            self.authority=Xrn.hrn_auth_list(self.hrn)


