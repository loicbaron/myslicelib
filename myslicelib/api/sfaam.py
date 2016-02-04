import traceback
import xmltodict
import uuid

from myslicelib.api.sfa import Api as SfaApi
from myslicelib.api.sfa import SfaError

def unique_call_id(): return uuid.uuid4().urn

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
    def __init__(self, url, pkey, email=None, hrn=None, certfile=None, verbose=False, timeout=None, reg=None):
        super(SfaAm, self).__init__(url, pkey, email, hrn, certfile, verbose, timeout)
        self.user_credential = reg.user_credential
        

    def get(self, hrn, obj_type):
        try:
            self.api_options = {'rspec_type': 'GENI', 'rspec_version': '3'}
            if obj_type == 'lease':
                self.api_options['list_leases']='all'
            if obj_type == 'resource' or obj_type == 'lease':
                result = self.ListResources([self.user_credential], self.api_options)
                # filter and return the resource or the lease
            elif obj_type == 'slice':
                self.api_options['list_leases']='all'
                if self.version()['geni_api'] == 2:
                    self.api_options['geni_slice_urn'] = hrn_to_urn(hrn)
                    result = server.ListResources([object_cred], self.api_options)
                elif self.version()['geni_api']==3:
                    result = self.Describe([urn], self.slice_credential, self.api_options)
                else:
                    raise NotImplementedError('geni_ api version not supported')
            else:
                raise NotImplementedError('Not implemented')

            if result['code']['geni_code'] == 0:
                dict_result = xmltodict.parse(result['value'])
                result['parsed'] = dict_result
            else:
                raise SfaError(result) 

        except Exception as e:
            traceback.print_exc()
            return False
        return result
    
    def list(self, obj_type):
        try:
            if obj_type == 'slice':
                raise NotImplementedError('List slices has to be sent to Registry not to AM')

            self.api_options = {'rspec_type': 'GENI', 'rspec_version': '3'}
            if obj_type == 'lease':
                self.api_options['list_leases'] = 'all'
            # All resource or lease
            if obj_type == 'resource' or obj_type == 'lease':
                result = self.ListResources([self.user_credential], self.api_options)
            else:
               raise NotImplementedError('Not implemented')

            if result['code']['geni_code'] == 0:
                dict_result = xmltodict.parse(result['value'])
                result['parsed'] = dict_result
            else:
                raise SfaError(result) 

        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def create(self, record_dict, obj_type):
        return self.update(record_dict, obj_type)

    def delete(self, hrn, obj_type):
        # self.Delete
        try:
            if obj_type == 'slice':
                result = server.Delete([urn] ,[self.slice_credential], self.api_options)
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def update(self, record_dict, obj_type):
        try:
            if obj_type == 'slice':
                # if update only expiration date
                # self.Renew
                if 'expiration_date' in record_dict:
                    date = record_dict['expiration_date']
                    result = server.Renew([urn] ,[object_cred], date, api_options)
                else:
                    self.api_options['call_id'] = unique_call_id()
                    api_options['sfa_users'] = record_dict['users']
                    api_options['geni_users'] = record_dict['users']

                    if type(record_dict['parsed']) is dict:
                        rspec = xmltodict.unparse(record_dict['parsed'])
                    else:
                        raise TypeError('parsed rspec has to be a dict') 
                    # self.CreateSliver (v2)
                    if self.version()['geni_api'] == 2:
                        result = server.CreateSliver([urn] ,[object_cred], rspec, api_options)
                    # v3
                    # self.Allocate
                    # self.Provision
                    elif self.version()['geni_api'] == 3:
                        result = server.Allocate(urn ,[object_cred], rspec, api_options)
                        result = server.Provision([urn] ,[object_cred], api_options)
                    else:
                        raise NotImplementedError('geni_ api version not supported')

                    if result['code']['geni_code'] == 0:
                        dict_result = xmltodict.parse(result['value'])
                        result['parsed'] = dict_result
                    else:
                        raise SfaError(result) 
            else:
                raise NotImplementedError('Not implemented')

        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def execute(self, hrn, action, obj_type):
        if action.lower() == 'shutdown':
            result = server.Shutdown(urn ,[object_cred], api_options)
        else:
            if self.version()['geni_api'] == 3:
                result = server.PerformOperationalAction([urn] ,[object_cred], action, api_options)
            else:
                raise NotImplementedError('This AM version does not support PerformOperationalAction')
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


