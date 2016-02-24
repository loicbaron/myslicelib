import traceback
import xmltodict
import uuid
import re
import xml.etree.ElementTree


from myslicelib.api.sfa import Api as SfaApi
from myslicelib.api.sfa import SfaError


def unique_call_id(): return uuid.uuid4().urn

def hrn_to_urn(hrn, type): return Xrn(hrn, type=type).urn

def urn_to_hrn(urn, type): return Xrn(urn, type=type).hrn

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

    def _construct_resource(self, xml_string):
        list_of_resource = []
        respec_root = xml.etree.ElementTree.fromstring(xml_string)
        for node in respec_root.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {}
            resource['hostname'] = node.attrib['component_name']
            resource['id'] = node.attrib['component_id']
            for element in list(node):
                if 'location' in element.tag:
                    resource['location'] = element.attrib
            list_of_resource.append(resource)
        return list_of_resource

    def _xml_to_dict(self, result):
        if result['code']['geni_code'] == 0:
            # there is a dictonary error while xmltodict

            if isinstance(result['value'], dict):
                #result['parsed'] = xmltodict.parse(result['value']['geni_rspec'])
                #print(result['value']['geni_rspec'])
                xml_string = result['value']['geni_rspec']
                result = self._construct_resource(xml_string) 
            else:
                xml_string = result['value']
                #print(xml_string)
                result = self._construct_resource(xml_string)
        else:
            raise SfaError(result)
        return result

    def get(self, hrn, obj_type):
        try:
            api_options = {}
            api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '3'}

            if obj_type == 'slice':
                urn = hrn_to_urn(hrn, obj_type)
                api_options['list_leases'] = 'all'
                self.slice_credential = self.registry.get_credential(hrn, obj_type)
                if self.version()['geni_api'] == 2:
                    api_options['geni_slice_urn'] = urn
                    result = self.proxy.ListResources([self.slice_credential], api_options)
                elif self.version()['geni_api'] == 3:
                    result = self.proxy.Describe([urn], self.slice_credential, api_options)
                else:
                    raise NotImplementedError('geni_api version not supported')
            else:
                result = self.list(obj_type)
            result = self._xml_to_dict(result)
        except Exception as e:
            traceback.print_exc()
            return False
        return result

    def list(self, obj_type):
        try:
            api_options = {}
            if obj_type == 'slice':
                raise NotImplementedError('List slices has to be sent to Registry not to AM')
            api_options['geni_rspec_version'] = {'type': 'GENI', 'version': '3'}
            if obj_type == 'lease':
                api_options['list_leases'] = 'all'
            # All resource or lease
            if obj_type == 'resource' or obj_type == 'lease':
                result = self.proxy.ListResources([self.registry.user_credential], api_options)
            else:
                raise NotImplementedError('Not implemented')
            result = self._xml_to_dict(result)
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


class Xrn:

    ########## basic tools on URNs
    URN_PREFIX = "urn:publicid:IDN"
    URN_PREFIX_lower = "urn:publicid:idn"

    ########## basic tools on HRNs
    # split a HRN-like string into pieces
    # this is like split('.') except for escaped (backslashed) dots
    # e.g. hrn_split ('a\.b.c.d') -> [ 'a\.b','c','d']
    @staticmethod
    def hrn_split(hrn):
        return [x.replace('--sep--', '\\.') for x in hrn.replace('\\.', '--sep--').split('.')]

    # e.g. hrn_leaf ('a\.b.c.d') -> 'd'
    @staticmethod
    def hrn_leaf(hrn): return Xrn.hrn_split(hrn)[-1]

    # e.g. hrn_auth_list ('a\.b.c.d') -> ['a\.b', 'c']
    @staticmethod
    def hrn_auth_list(hrn): return Xrn.hrn_split(hrn)[0:-1]

    # e.g. escape ('a.b') -> 'a\.b'
    @staticmethod
    def escape(token): return re.sub(r'([^\\])\.', r'\1\.', token)

    # e.g. unescape ('a\.b') -> 'a.b'
    @staticmethod
    def unescape(token): return token.replace('\\.', '.')

    def __init__(self, xrn="", type=None, id=None):
        if not xrn:
            xrn = ""
        # user has specified xrn : guess if urn or hrn
        self.id = id
        if Xrn.is_urn(xrn):
            self.hrn = None
            self.urn = xrn
            if id:
                self.urn = "%s:%s" % (self.urn, str(id))
            self.urn_to_hrn()
        else:
            self.urn = None
            self.hrn = xrn
            self.type = type
            self.hrn_to_urn()
        self._normalize()

    def _normalize(self):
        if self.hrn is None:
            raise(SfaError, "Xrn._normalize")
        if not hasattr(self, 'leaf'):
            self.leaf = Xrn.hrn_split(self.hrn)[-1]
        # self.authority keeps a list
        if not hasattr(self, 'authority'):
            self.authority = Xrn.hrn_auth_list(self.hrn)

    def get_authority_hrn(self):
        self._normalize()
        return '.'.join(self.authority)

    def get_authority_urn(self):
        self._normalize()
        return ':'.join([Xrn.unescape(x) for x in self.authority])

    @staticmethod
    def is_urn(text):
        return text.lower().startswith(Xrn.URN_PREFIX_lower)

    def hrn_to_urn(self):
        """
        compute urn from (hrn, type)
        """

        #if not self.hrn or self.hrn.startswith(Xrn.URN_PREFIX):
        if Xrn.is_urn(self.hrn):
            raise SfaError("Xrn.hrn_to_urn, hrn=%s"%self.hrn)

        if self.type and self.type.startswith('authority'):
            self.authority = Xrn.hrn_auth_list(self.hrn)
            leaf = self.get_leaf()
            #if not self.authority:
            #    self.authority = [self.hrn]
            type_parts = self.type.split("+")
            self.type = type_parts[0]
            name = 'sa'
            if len(type_parts) > 1:
                name = type_parts[1]
            auth_parts = [part for part in [self.get_authority_urn(), leaf] if part]
            authority_string = ":".join(auth_parts)
        else:
            self.authority = Xrn.hrn_auth_list(self.hrn)
            name = Xrn.hrn_leaf(self.hrn)
            authority_string = self.get_authority_urn()

        if self.type is None:
            urn = "+".join(['', authority_string, Xrn.unescape(name)])
        else:
            urn = "+".join(['', authority_string, self.type, Xrn.unescape(name)])

        if hasattr(self, 'id') and self.id:
            urn = "%s:%s" % (urn, self.id)

        self.urn = Xrn.URN_PREFIX + urn

    def urn_to_hrn(self):
        """
        compute tuple (hrn, type) from urn
        """
        # if not self.urn or not self.urn.startswith(Xrn.URN_PREFIX):
        if not Xrn.is_urn(self.urn):
            raise SfaError("Xrn.urn_to_hrn")

        parts = Xrn.urn_split(self.urn)
        type = parts.pop(2)
        # Remove the authority name (e.g. '.sa')
        if type == 'authority':
            name = parts.pop()
            # Drop the sa. This is a bad hack, but its either this
            # or completely change how record types are generated/stored   
            if name != 'sa':
                type = type + "+" + name
            name = ""
        else:
            name = parts.pop(len(parts)-1)
        # convert parts (list) into hrn (str) by doing the following
        # 1. remove blank parts
        # 2. escape dots inside parts
        # 3. replace ':' with '.' inside parts
        # 3. join parts using '.'
        hrn = '.'.join([Xrn.escape(part).replace(':', '.') for part in parts if part])
        # dont replace ':' in the name section
        if name:
            parts = name.split(':')
            if len(parts) > 1:
                self.id = ":".join(parts[1:])
                name = parts[0]
            hrn += '.%s' % Xrn.escape(name)
        self.hrn = str(hrn)
        self.type = str(type)

