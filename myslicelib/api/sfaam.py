import traceback
import xmltodict
import xml.etree.ElementTree

from myslicelib.util.sfa import hrn_to_urn
from myslicelib.api.sfa import Api as SfaApi
from myslicelib.api.sfa import SfaError




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


    def _parse_resource(self, xml_string):
        result = []
        respec_root = xml.etree.ElementTree.fromstring(xml_string)
        for node in respec_root.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {
                'hostname': node.attrib['component_name'],
                'id': node.attrib['component_id']
            }
            for element in list(node):
                if 'location' in element.tag:
                    resource['location'] = element.attrib
            result.append(resource)
        return result

    def _parse_slice(self, xml_string):
        return self._parse_resource(xml_string)

    def _lease(self, hrn=None):
        return self.proxy.ListResources([self.registry.user_credential],
                                        {
                                            'list_leases' : 'all',
                                            'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
                                        })

    def _resource(self, hrn=None):
        return self.proxy.ListResources([self.registry.user_credential],
                                        {
                                            'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
                                        })

    def _slice(self, hrn):
        urn = hrn_to_urn(hrn, 'slice')
        options = {
                    'list_leases' : 'all',
                    'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
                }
        slice_credential = self.registry.get_credential(hrn, 'slice')

        if self.version()['geni_api'] == 2:
            options['geni_slice_urn'] = urn
            return self.proxy.ListResources([slice_credential], options)
        elif self.version()['geni_api'] == 3:
            return self.proxy.Describe([urn], slice_credential, options)
        else:
            raise NotImplementedError('geni_api version not supported')


    def get(self, entity, hrn=None, raw=False):

        try:
            result = getattr(self, "_" + entity)(hrn)
        except Exception as e:
            print(e)
            exit(1)

        if raw:
            return result

        # check gene error codes
        if result['code']['geni_code'] == 0:
            try:
                if isinstance(result['value'], dict):
                    xml_string = result['value']['geni_rspec']
                else:
                    xml_string = result['value']
                result = getattr(self, "_parse_" + entity)(xml_string)
            except Exception as e:
                print(e)
                exit(1)
        else:
            raise SfaError(result)

        return result



    def create(self, record_dict, obj_type):
        return self.update(record_dict, obj_type)

    def delete(self, hrn, obj_type):
        # self.Delete
        try:
            if obj_type == 'slice':
                urn = hrn_to_urn(hrn, obj_type)
                self.slice_credential = self.registry.get_credential(hrn, obj_type)
                #*self.ois(server, api_options) to check server if uuid supported
                api_options = {}
                result = self.proxy.Delete([urn], [self.slice_credential], api_options)
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def update(self, record_dict, obj_type):
        try:
            if obj_type == 'slice':
                urn = hrn_to_urn(record_dict['hrn'], obj_type)
                self.slice_credential = self.registry.get_credential(record_dict['hrn'], obj_type)
                # if update only expiration date
                # self.Renew
                if 'expiration_date' in record_dict:
                    date = record_dict['expiration_date']
                    result = self.proxy.Renew([urn], [object_cred], date, api_options)
                else:
                    api_options = {}
                    api_options['call_id'] = unique_call_id()
                    api_options['sfa_users'] = record_dict['users']
                    api_options['geni_users'] = record_dict['users']
                    #api_options['append'] = True

                    if isinstance(record_dict['parsed'], dict):
                        rspec = xmltodict.unparse(record_dict['parsed'])
                    else:
                        raise TypeError('parsed rspec has to be a dict') 
                    
                    # self.CreateSliver (v2)
                    if self.version()['geni_api'] == 2:
                        api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '2'}
                        result = self.proxy.CreateSliver([urn] ,[object_cred], rspec, api_options)
                    # v3
                    # self.Allocate
                    # self.Provision
                    elif self.version()['geni_api'] == 3:
                        api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '3'}
                        result = self.proxy.Allocate(urn, [self.slice_credential], rspec, api_options)
                        api_options['call_id'] = unique_call_id()
                        result = self.proxy.Provision([urn], [self.slice_credential], api_options)
                    else:
                        raise NotImplementedError('geni_ api version not supported')                  
                    result = self._xml_to_dict(result)
            else:
                raise NotImplementedError('Not implemented')
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def execute(self, hrn, action, obj_type):
        urn = hrn_to_urn(hrn, obj_type)
        if action.lower() == 'shutdown':
            result = self.proxy.Shutdown(urn, [object_cred], api_options)
        else:
            if self.version()['geni_api'] == 3:
                result = self.proxy.PerformOperationalAction([urn], [object_cred], action, api_options)
            else:
                raise NotImplementedError('This AM version does not support PerformOperationalAction')
        return result




