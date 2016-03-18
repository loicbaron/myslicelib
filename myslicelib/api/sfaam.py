import traceback
from pprint import pprint
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, unique_call_id
from myslicelib.util.builder import Builder
from myslicelib.util.parser import Parser
from myslicelib.api.sfa import Api as SfaApi
from myslicelib.api.sfa import SfaError
from myslicelib.error import MysParameterIsRequiredError

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

    def __init__(self, endpoint=None, registry=None):
        super(SfaAm, self).__init__(endpoint, registry.credential)
        self.registry = registry

    def _lease(self, urn=None):
        # lease don't have urn, it has a lease_id in OMF (hash), but no id in IoT-Lab
        if self.version()['version'] == 2:
            cred = self.registry.user_credential
        else:
            cred = {'geni_value': self.registry.user_credential, 'geni_version': '3', 'geni_type': 'geni_sfa'}
        # XXX Check result
        return self._proxy.ListResources([cred],
                                        {
                                            'list_leases' : 'all',
                                            'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
                                        })

    def _resource(self, urn=None):
        if self.version()['version'] == 2:
            cred = self.registry.user_credential
        else:
            cred = {'geni_value': self.registry.user_credential, 'geni_version': '3', 'geni_type': 'geni_sfa'}
        # XXX Check result
        return self._proxy.ListResources([cred],
                                        {
                                            'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
                                        })

    def _slice(self, urn):
        # urn can't be None for slice
        if urn is None:
            raise Exception('Slice urn must be specified')
        hrn = urn_to_hrn(urn)[0]
        options = {
                    'list_leases' : 'all',

                    'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
                }
        slice_credential = self.registry.get_credential(hrn, 'slice')

        if self.version()['version'] == 2:
            options['geni_slice_urn'] = urn
            # XXX Check result
            return self._proxy.ListResources([slice_credential], options)
        elif self.version()['version'] == 3:
            # XXX Check result
            return self._proxy.Describe([urn], [slice_credential], options)
        else:
            raise NotImplementedError('geni_api version not supported')


    def get(self, entity, urn=None, raw=False):

        try:
            result = getattr(self, "_" + entity)(urn)
        except Exception as e:
            traceback.print_exc()
            exit(1)

        if raw:
            return result

        # check geni error codes
        if result['code']['geni_code'] == 0:
            try:
                if isinstance(result['value'], dict):
                    xml_string = result['value']['geni_rspec']
                else:
                    xml_string = result['value']
                # from pprint import pprint
                # pprint(xml_string)
                # XXX if urn is not None we need to Filter - in the parser??? 
                result = Parser(xml_string).parse(entity)
                # XXX Check result
            except Exception as e:
                traceback.print_exc()
                exit(1)
        else:
            raise SfaError(result)

        return result


    def create(self, entity, urn, record_dict):
        return self.update(entity, urn, record_dict)

    def delete(self, entity, urn):
        # self.Delete
        try:
            if entity == 'slice':
                hrn = urn_to_hrn(urn)[0]
                self.slice_credential = self.registry.get_credential(hrn, entity)
                #*self.ois(server, api_options) to check server if uuid supported
                api_options = {}
                result = self._proxy.Delete([urn], [self.slice_credential], api_options)
                # XXX Check result
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def update(self, entity, urn, record_dict):
        try:
            if entity == 'slice':
                hrn = urn_to_hrn(urn)[0]
                self.slice_credential = self.registry.get_credential(hrn, entity)
                # if update only expiration date
                # self.Renew
                if 'expiration_date' in record_dict:
                    date = record_dict['expiration_date']
                    result = self._proxy.Renew([urn], [object_cred], date, api_options)
                else:
                    api_options = {}
                    api_options['call_id'] = unique_call_id()
                    api_options['sfa_users'] = record_dict['geni_users']
                    api_options['geni_users'] = record_dict['geni_users']
                    #api_options['append'] = True
                    pprint(api_options)

                    rspec = Builder(self.version()['testbed']).build(urn, record_dict)

                    #if 'parsed' not in record_dict:
                    #    raise MysParameterIsRequiredError('request respec is required')
                    #if isinstance(record_dict['parsed'], dict):
                    #    rspec = xmltodict.unparse(record_dict['parsed'])
                    #else:
                    #    raise TypeError('parsed rspec has to be a dict') 
                    
                    # self.CreateSliver (v2)
                    if self.version()['version'] == 2:
                        api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '2'}
                        result = self._proxy.CreateSliver([urn] ,[object_cred], rspec, api_options)
                    # v3
                    # self.Allocate
                    # self.Provision
                    elif self.version()['version'] == 3:
                        api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '3'}
                        result = self._proxy.Allocate(urn, [self.slice_credential], rspec, api_options)
                        pprint(result)
                        if 'code' in result and 'geni_code' in result['code'] and result['code']['geni_code']==0:
                            api_options['call_id'] = unique_call_id()
                            result = self._proxy.Provision([urn], [self.slice_credential], api_options)
                        else:
                            raise SfaError(result)
                    else:
                        raise NotImplementedError('geni_ api version not supported')                  
                    pprint(result)
                    # check geni error codes
                    if result['code']['geni_code'] == 0:
                        try:
                            if isinstance(result['value'], dict):
                                xml_string = result['value']['geni_rspec']
                            else:
                                xml_string = result['value']
                            # from pprint import pprint
                            # pprint(xml_string)
                            # XXX if urn is not None we need to Filter - in the parser??? 
                            result = Parser(xml_string).parse(entity)
                            # XXX Check result
                        except Exception as e:
                            traceback.print_exc()
                            exit(1)
                    else:
                        raise SfaError(result)

            else:
                raise NotImplementedError('Not implemented')
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def execute(self, urn, action, obj_type):
        if action.lower() == 'shutdown':
            # XXX Check result
            result = self._proxy.Shutdown(urn, [object_cred], api_options)
        else:
            if self.version()['version'] == 3:
                # XXX Check result
                result = self._proxy.PerformOperationalAction([urn], [object_cred], action, api_options)
            else:
                raise NotImplementedError('This AM version does not support PerformOperationalAction')
        return result




