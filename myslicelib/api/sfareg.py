import os
import traceback
import pytz

from myslicelib.api.sfa import Api as SfaApi
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn 

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError

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
        tz = pytz.timezone('Europe/Paris')
        return tz.localize(date)

    def _slice(self, data):
        slices = []
        for d in data:

            # users urn
            users = []
            for u in d.get('reg-researchers', []):
                users.append(hrn_to_urn(u, 'user'))

            slices.append({
                'id': d['reg-urn'],
                'shortname': d['hrn'].split('.')[-1],
                'hrn': d['hrn'],
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
                'id' :  d.get('reg-urn'),
                'shortname': d['hrn'].split('.')[-1],
                'hrn': d['hrn'],
                'name': d['name'],
                'certificate': d['gid'],
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

                'id' :  d['reg-urn'],
                'shortname': d['hrn'].split('.')[-1],
                'hrn': d['hrn'],
                'name': d['name'],
                'certificate': d['gid'],
                'created': self._datetime(d['date_created']),
                'updated': self._datetime(d['last_updated']),
                'pi_users': [hrn_to_urn(user, 'user') for user in d['reg-pis']],
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
            'hrn': d['hrn'],
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
            if entity == urn_type or entity == 'project':
                result = self._get_entity(hrn)
            else:
                raise MysNotImplementedError('Please check %s is %s' % (urn, entity))

        if raw:
            return self._extract_with_entity(entity, result)

        try:
            result = getattr(self, "_" + entity)(result)
        except Exception as e:
            traceback.print_exc()
            exit(1)

        return result

    # look up to see the upper has the credential
    def get_credential(self, hrn, entity):
        try:
            upper_hrn = '.'.join(hrn.split('.')[:-1])
            if hrn:
                if entity == 'slice':
                    return self._proxy.GetCredential(self.user_credential, hrn, entity)
                return self._proxy.GetCredential(self.user_credential, upper_hrn, entity)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
            return self.get_credential(upper_hrn, entity)

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
            auth_cred = self.get_credential(hrn, 'authority')
            if auth_cred:
                mapped_dict = getattr(self, '_'+entity+'_mappings')(hrn, record_dict)
                print(mapped_dict)
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
            if entity == 'user' and hrn == self.credential.hrn:
                cred = self.user_credential
            elif entity == 'slice':
                cred = self.get_credential(hrn, 'slice')
            else:
                cred = self.get_credential(hrn, 'authority')
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
            auth_cred = self.get_credential(hrn, 'authority')
            if auth_cred:
                result = self._proxy.Remove(hrn, auth_cred, entity)
                if result != 1:
                    raise Exception(result)
                return []
        except Exception as e:
            traceback.print_exc()
            return []

    # self.CreateGid
