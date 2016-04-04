import os
import traceback
import pytz

from datetime import datetime
import dateutil.parser
import xml.etree.ElementTree

from myslicelib.api.sfa import Api as SfaApi
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn 

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError

class SfaReg(SfaApi):

    def __init__(self, endpoint, authentication):
        super(SfaReg, self).__init__(endpoint, authentication)
        if os.path.isfile(authentication.certificate):
            with open(authentication.certificate, "r") as myfile:
                certificate = myfile.read()
        else:
            certificate = authentication.certificate

        self.authentication = authentication

        self.user_credentials = []
        self.user_credential = None
        # this dict can contain: user_credential, slice_credential, authority_credential...
        # sfa_credentials can be delegated from another user
        if hasattr(authentication, 'credentials'):
            for c in authentication.credentials:
                if 'id' not in c:
                    c['id'] = hrn_to_urn(c['hrn'],c['type'])
                if 'hrn' not in c:
                    c['hrn'],c['type'] = urn_to_hrn(c['id'])
                if os.path.isfile(c['xml']):
                    with open(c['xml'], "r") as myfile:
                        c['xml'] = myfile.read()
                # Check if the credential is expired
                el = xml.etree.ElementTree.fromstring(c['xml'])
                expiration = el.find('credential').find('expires').text
                exp = dateutil.parser.parse(expiration)
                utc = pytz.utc
                if exp > utc.localize(datetime.now()):
                    self.user_credentials.append(c)
                    if c['type'] == 'user':
                        self.user_credential = c['xml']
                else:
                    print(k+': is expired')
        if not self.user_credential:
            print('GetSelfCredential from Registry')
            self.user_credential = self._proxy.GetSelfCredential(
                                        certificate,
                                        self.authentication.hrn,
                                        'user')
    def _getXmlCredential(self, hrn, obj_type):
        for c in self.user_credentials:
            if c['hrn']==hrn and c['type']==obj_type:
                return c['xml']
        return False

    def _extract_with_entity(self, entity, result):
        filtered_entites = []
        
        for record in result:
            if entity == 'project':
                if record['type'] == 'authority' and len(record['hrn'].split('.'))>2:
                    filtered_entites.append(record)
            
            elif entity == 'authority':
                if len(record['hrn'].split('.')) <3:
                    filtered_entites.append(record)

            elif record['type'] == entity:
                filtered_entites.append(record)
        return filtered_entites

    def _extract_with_authority(self, hrn, result):
        filtered_records = []
        for record in result:
            if record['authority'] == hrn:
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
        return self._proxy.Resolve(hrn, self.user_credential, {})

    def _datetime(self, date):
        '''
        Datetime objects must have a timezone

        :param date:
        :return:
        '''
        # TODO: use local timezone from server
        tz = pytz.timezone('UTC')
        return tz.localize(date)

    def _slice(self, data):
        slices = []
        for d in data:

            # users urn
            users = []
            for u in d.get('reg-researchers', []):
                users.append(hrn_to_urn(u, 'user'))

            slices.append({
                'id' : d.get('reg-urn'),
                'shortname': d.get('hrn').split('.')[-1],
                'hrn': d.get('hrn'),
                'created': self._datetime(d['date_created']),
                'updated': self._datetime(d['last_updated']),
                'users': users,
                'authority': hrn_to_urn(d['authority'], 'authority'),
                'project': hrn_to_urn('.'.join(d['hrn'].split('.')[:-1]), 'authority'),
            })
        return slices

    def _authority(self, data):
        authority = []
        for d in data:

            mappings = {
                'slice': [],
                'user': [],
                'authority': [],
            }
            ### XXX need optimatiztion with query(id = None)
            enitities = self._extract_with_authority(d['hrn'], self._list_entity(d['hrn']))

            for entity in enitities:
                # depend object tpye, we add this object urn to its coresponding mappings
                mappings[entity['type']] += [entity['reg-urn']]

            authority.append({
                'id': d.get('reg-urn'),
                'shortname': d.get('hrn').split('.')[-1],
                'hrn': d.get('hrn'),
                'name': d.get('name'),
                'certificate': d.get('gid'),
                'created': self._datetime(d['date_created']),
                'updated': self._datetime(d['last_updated']),
                'pi_users': [hrn_to_urn(user, 'user') for user in d.get('reg-pis', [])],
                'users': mappings['user'],
                'slices': mappings['slice'],
                'projects': mappings['authority']
            })
        return authority

    def _project(self, data):
        project = []
        
        for d in data:

            enitities = self._extract_with_authority(d['hrn'], self._list_entity(d['hrn']))

            mappings = {
                'slice': [],
                'user': [],
            }

            for entity in enitities:
                # depend object tpye, we add this object urn to its coresponding mappings
                if entity['type'] in mappings:
                    mappings[entity['type']]+= [entity['reg-urn']]

            project.append({
                'id' :  d.get('reg-urn'),
                'shortname': d.get('hrn').split('.')[-1],
                'hrn': d.get('hrn'),
                'name': d.get('name'),
                'certificate': d.get('gid'),
                'created': self._datetime(d['date_created']),
                'updated': self._datetime(d['last_updated']),
                'pi_users': [hrn_to_urn(user, 'user') for user in d.get('reg-pis', [])],
                'users': mappings['user'],
                'slices': mappings['slice'],
            })

        return project

    def _user(self, data):
        user = []

        for d in data:
            user.append({

            'id' :  d.get('reg-urn'),
            'shortname': d['hrn'].split('.')[-1],
            'hrn': d.get('hrn'),
            'keys': d.get('reg-keys', []),
            'certificate': d.get('gid'),
            'email': d.get('email', ''),
            'created': self._datetime(d['date_created']),
            'updated': self._datetime(d['last_updated']),
            'authority': hrn_to_urn(d['authority'], 'authority'),
            'pi_authorities': [ 
                                hrn_to_urn(pi_auth, 'authority') for pi_auth in d.get('reg-pi-authorities', [])
                               ],
            'slices': [
                        hrn_to_urn(sli, 'slice') for sli in d.get('reg-slices', [])
                    ],

            })

        return user

    def get(self, entity, urn=None, raw=False):

        result = []
        if urn is None:
            result = self._extract_with_entity(entity, self._list_entity())
        else:
            hrn, urn_type = urn_to_hrn(urn)

            if urn_type not in ['slice', 'user', 'authority']:
                raise MysNotUrnFormatError
            # entity is query object
            # urn_type is type of object derived from urn
            
            if entity != urn_type:
                if entity != 'project' or urn_type != 'authority':
                    raise MysNotImplementedError('Please check %s is %s' % (urn, entity))
            
            result = self._get_entity(hrn)

        if raw:
            return self._extract_with_entity(entity, result)

        try:
            result = getattr(self, "_" + entity)(result)
        except Exception as e:
            traceback.print_exc()
            exit(1)

        return result

    def get_credential(self, urn, delegated_to=None):
        hrn, entity = urn_to_hrn(urn)
        if delegated_to:
            local_cred = list(filter(lambda c: c['id'] == urn and c['delegated_to']==delegated_to, self.user_credentials))
        else:
            local_cred = list(filter(lambda c: c['id'] == urn, self.user_credentials))

        if local_cred:
            print('already defined %s' % urn)
            return local_cred
        else:
            if delegated_to:
                # XXX To be removed
                cred = self._proxy.GetCredential(self.user_credential, hrn, entity),
                # TODO
                # delegate(cred)
                # gid of object urn
                #obj_gid = self._proxy.GetGids([hrn], self.user_credential)
                #user_pkey = self.authentication.private_key
                # gid of user
                #user_gid = self._proxy.GetGids([self.authentication.hrn], self.user_credential)
                #cred = delegate(obj_gid_file, user_pkey_file, user_gid_file)
            else:
                cred = self._proxy.GetCredential(self.user_credential, hrn, entity),
            d = [{
                'id': urn,
                'type': entity,
                'xml': cred, 
                'delegated_to': delegated_to,
            }]
            self.user_credentials += d 
        return d

    # look up to see the upper has the credential
    def search_credential(self, hrn, entity):
        try:
            upper_hrn = '.'.join(hrn.split('.')[:-1])
            if hrn:
                if entity == 'slice':
                    # If credentials were provided don't call the Registry
                    c = self._getXmlCredential(hrn, entity)
                    if c: return c
                    print('GetCredential hrn: '+hrn+' from Registry')
                    return self._proxy.GetCredential(self.user_credential, hrn, entity)
                # If credentials were provided don't call the Registry
                c = self._getXmlCredential(upper_hrn, entity)
                if c: return c
                if not upper_hrn or obj_type is None:
                    upper_hrn = hrn
                print('GetCredential upper: '+upper_hrn+' from Registry')
                return self._proxy.GetCredential(self.user_credential, upper_hrn, entity)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
            return self.search_credential(upper_hrn, entity)

    def _user_mappings(self, hrn, record_dict):
        mapped_dict = {
                    'hrn': hrn,
                    'type': 'user',                 
                    'email': record_dict.get('email', ''), # email cant be empty string                  
        }

        if 'keys' in record_dict:
            mapped_dict['keys'] = record_dict.get('keys', '')
        return mapped_dict

    def _authority_mappings(self, hrn, record_dict):
        mapped_dict = {
                    'hrn': hrn,
                    'type': 'authority',                 
                    'name': record_dict.get('name', None),
                    'reg-pis': record_dict.get('pi_users', [])                   
        }
        return mapped_dict

    def _slice_mappings(self, hrn, record_dict):

        mapped_dict = {
                    'hrn': hrn,
                    'type': 'slice',          
                    'reg-researchers': record_dict.get('users', []),
        }
        return mapped_dict

    def create(self, entity, urn, record_dict):
        try:
            hrn = urn_to_hrn(urn)[0]
            auth_cred = self.search_credential(hrn, 'authority')
            if auth_cred:
                mapped_dict = getattr(self, '_'+entity+'_mappings')(hrn, record_dict)
                result = self._proxy.Register(mapped_dict, auth_cred)
                # XXX test the result either 1 or a gid
                return self.get(entity, urn)
            return []
        except Exception as e:
            traceback.print_exc()
            return []

    def update(self, entity, urn, record_dict):
        hrn = urn_to_hrn(urn)[0]
        try:
            if entity == 'user' and hrn == self.authentication.hrn:
                cred = self.user_credential
            elif entity == 'slice':
                cred = self.search_credential(hrn, 'slice')
            else:
                cred = self.search_credential(hrn, 'authority')
            if cred:
                mapped_dict = getattr(self, '_'+entity+'_mappings')(hrn, record_dict)
                result = self._proxy.Update(mapped_dict, cred)
                # XXX test the result either 1 or a gid
                return self.get(entity, urn)
            raise Exception("No Credential to update this Or Urn is Not Right", urn)
        except Exception as e:
            traceback.print_exc()
            return []

    def delete(self, entity, urn):
        try:
            hrn = urn_to_hrn(urn)[0]
            auth_cred = self.search_credential(hrn, 'authority')
            if auth_cred:
                result = self._proxy.Remove(hrn, auth_cred, entity)
                if result != 1:
                    raise Exception(result)
            return []
        except Exception as e:
            traceback.print_exc()
            return []

    # self.CreateGid
