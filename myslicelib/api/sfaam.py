import traceback
from pprint import pprint
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn, unique_call_id
from myslicelib.util.builder import Builder
from myslicelib.util.parser import Parser, get_testbed_type
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
        super(SfaAm, self).__init__(endpoint, registry.authentication)
        self.registry = registry

    def _lease(self, urn=None):
        # lease don't have urn, it has a lease_id in OMF (hash), but no id in IoT-Lab
        if self._version['geni_api'] == 2:
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
        if self._version['geni_api'] == 2:
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
        slice_credential = self.registry.search_credential(hrn, 'slice')

        if self._version['geni_api'] == 2:
            options['geni_slice_urn'] = urn
            # XXX Check result
            return self._proxy.ListResources([slice_credential], options)
        elif self._version['geni_api'] == 3:
            # XXX Check result
            return self._proxy.Describe([urn], [slice_credential], options)
        else:
            raise NotImplementedError('geni_api version not supported')


    def get(self, entity, urn=None, raw=False):
        try:
            result = getattr(self, "_" + entity)(urn)
        except Exception as e:
            result = []
            #traceback.print_exc()
            self.logs.append({
                            'endpoint': self.endpoint.name,
                            'url': self.endpoint.url,
                            'protocol': self.endpoint.protocol,
                            'type': self.endpoint.type,
                            'exception': str(e)
                            })

        if not raw:
            result = self._parse_xml(result, entity)
        
        return {'data':result,'errors':self.logs}

    def _parse_xml(self, result, entity):
        try: 
            # No result means that we already had an error (ex: Time Out)
            if not result:
                return result
            # check geni error codes
            if self.isResultOk(result):
                if isinstance(result['value'], dict):
                    xml_string = result['value']['geni_rspec']
                else:
                    xml_string = result['value']
                # pprint(xml_string)
                # XXX if urn is not None we need to Filter - in the parser??? 
                testbed = get_testbed_type(self._version['urn'])
                result = Parser(testbed, xml_string).parse(entity)
                return result
                # XXX Check result
            else:
                raise SfaError(result)
        except Exception as e:
            traceback.print_exc()
            self.logs.append({
                            'endpoint': self.endpoint.name,
                            'url': self.endpoint.url,
                            'protocol': self.endpoint.protocol,
                            'type': self.endpoint.type,
                            'exception': str(e)
                            })
            if entity == 'slice':
                return [{'resources':[],'leases':[]}]
            else:
                return []


    def create(self, entity, urn, record_dict):
        return self.update(entity, urn, record_dict)

    def delete(self, entity, urn):
        # self.Delete
        result = []
        try:
            if entity != 'slice':
                raise NotImplementedError('Not implemented')
            
            hrn = urn_to_hrn(urn)[0]
            slice_credential = self.registry.search_credential(hrn, 'slice')

            #*self.ois(server, api_options) to check server if uuid supported
            api_options = {}
            res = self._proxy.Delete([urn], [slice_credential], api_options)
            if self.isResultOk(res):
                result = []
            else:
                raise Exception(res)
            # XXX Check result
        except Exception as e:
            traceback.print_exc()
            self.logs.append({
                            'endpoint': self.endpoint.name,
                            'url': self.endpoint.url,
                            'protocol': self.endpoint.protocol,
                            'type': self.endpoint.type,
                            'exception': str(e)
                            })
        return {'data':result,'errors':self.logs}

    def _renew_slice(self, urn, record_dict, api_options):
        # renew

        date = record_dict['expiration_date']
        
        return self._proxy.Renew([urn], [slice_credential], date, api_options)

    def _update_slice_v2(self, urn, rspec, api_options):
        # v2 sfa update
        
        api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '2'}
        
        return self._proxy.CreateSliver([urn] ,[self.slice_credential], rspec, api_options)
        
    def _update_slice_v3(self, urn, rspec, api_options):
        # v3 sfa update
        
        api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '3'}
        result = self._proxy.Allocate(urn, [self.slice_credential], rspec, api_options)
        if self.isResultOk(result):
            # another call id 
            api_options['call_id'] = unique_call_id()
            return self._proxy.Provision([urn], [self.slice_credential], api_options)
        else:
            raise SfaError(result)

    def update(self, entity, urn, record_dict):
        result = []
        try:
            if entity != 'slice':
                raise NotImplementedError('Not implemented')

            if 'run_am' in record_dict and record_dict['run_am']:
                # slice_cred would be a dict, here for simple test, we just return cred
                self.slice_credential = self.registry.get_credential(urn, raw=True)

                api_options = {
                    'call_id': unique_call_id(),
                    'sfa_users': record_dict['geni_users'],
                    'geni_users': record_dict['geni_users'],
                    # api_options['append'] = True
                }

                if 'expiration_date' in record_dict:
                    result = self._renew_slice(urn, record_dict, api_options)
                parser = get_testbed_type(self._version['urn'])
                rspec = Builder(parser, self._version['urn']).build(urn, record_dict)

                if self._version['geni_api'] == 2:
                    result = self._update_slice_v2(urn, rspec, api_options)

                elif self._version['geni_api'] == 3:
                    result = self._update_slice_v3(urn, rspec, api_options)

                else:
                    raise NotImplementedError('geni_ api version not supported')

                result = self._parse_xml(result, 'slice')

        except Exception as e:
            traceback.print_exc()
            self.logs.append({
                            'endpoint': self.endpoint.name,
                            'url': self.endpoint.url,
                            'protocol': self.endpoint.protocol,
                            'type': self.endpoint.type,
                            'exception': str(e)
                            })
        return {'data':result,'errors':self.logs}

    def execute(self, urn, action, obj_type):
        result = []
        try:
            if action.lower() == 'shutdown':
                res = self._proxy.Shutdown(urn, [object_cred], api_options)
                # XXX Check res
                # TODO: raise Exception(res)
            else:
                if self._version['geni_api'] == 3:
                    res = self._proxy.PerformOperationalAction([urn], [object_cred], action, api_options)
                    # XXX Check res
                    # TODO: raise Exception(res)
                else:
                    raise NotImplementedError('This AM version does not support PerformOperationalAction')
        except Exception as e:
            traceback.print_exc()
            self.logs.append({
                            'endpoint': self.endpoint.name,
                            'url': self.endpoint.url,
                            'protocol': self.endpoint.protocol,
                            'type': self.endpoint.type,
                            'exception': str(e)
                            })

        return {'data':result,'errors':self.logs}

    def isResultOk(self, result):
        if 'code' in result and \
            'geni_code' in result['code'] and \
            result['code']['geni_code']==0:
            return True
        else:
            return False

