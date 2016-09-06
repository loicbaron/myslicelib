import os
import tempfile
import pytz
import collections

from sfa.trust.credential import Credential
from sfa.trust.gid import GID

from pprint import pprint

from datetime import datetime
import dateutil.parser
import xml.etree.ElementTree

from myslicelib.api.sfa import Api as SfaApi
from myslicelib.api.sfa import SfaError
from myslicelib.util.sfa import hrn_to_urn, urn_to_hrn

from myslicelib.error import MysNotUrnFormatError
from myslicelib.error import MysNotImplementedError


def is_user(record):
    return record['classtype'] == 'user'


def is_silce(record):
    return record['classtype'] == 'slice'


def is_authority(record):
    if record['classtype'] == 'authority':
        return (len(record['hrn'].split('.')) < 3)


def is_project(record):
    if record['classtype'] == 'authority':
        return (len(record['hrn'].split('.')) > 2)


class SfaReg(SfaApi):

    _types = ['slice', 'user', 'authority']

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
                if 'xml' in c and isinstance(c['xml'], str) and os.path.isfile(c['xml']):
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
                    #print(c['id'] +': is expired')
                    pass

        if not self.user_credential:
            #print('GetSelfCredential from Registry')
            self.user_credential = self._proxy.GetSelfCredential(
                                        certificate,
                                        self.authentication.hrn,
                                        'user')

    def _getXmlCredential(self, hrn, obj_type):
        for c in self.user_credentials:
            if c['hrn']==hrn and c['type']==obj_type:
                return c['xml']
        return False

    def _datetime(self, date):
        '''
        Datetime objects must have a timezone

        :param date:
        :return:
        '''
        # TODO: use local timezone from server
        tz = pytz.timezone('UTC')
        return tz.localize(date)

    def _filter_authority(self, records):
        authorities = collections.defaultdict(dict)
        for record in records:
            if is_authority(record):
                auth = record['hrn']
                authorities[auth].update(record)

            auth = record['authority']
            if auth is not None and len(auth.split('.')) < 3:

                if is_project(record):
                    authorities[auth].setdefault('projects', []) \
                                     .append(record['reg-urn'])

                if is_user(record):
                    authorities[auth].setdefault('users', []) \
                                     .append(record['reg-urn'])

                if is_silce(record):
                    authorities[auth].setdefault('slices', []) \
                                     .append(record['reg-urn'])

        # return a list of authority obj
        return [data for data in authorities.values()]

    def _filter_project(self, records):
        projects = collections.defaultdict(dict)
        for record in records:
            if is_project(record):
                proj = record['hrn']
                projects[proj].update(record)

            # project is just a variant of authority
            proj = record['authority']
            if proj is not None and len(proj.split('.')) > 2:

                if is_user(record):
                    projects[proj].setdefault('users', []) \
                                  .append(record['reg-urn'])

                if is_silce(record):
                    projects[proj].setdefault('slices', []) \
                                  .append(record['reg-urn'])

        return [data for data in projects.values()]

    def _get_entities(self, entity):
        version = self._proxy.GetVersion()
        platform_urn = version['urn']

        records = self._proxy.List(platform_urn, self.user_credential,
                                   {'recursive': True})
        if entity == 'authority':
            result = self._filter_authority(records)

        if entity == 'project':
            result = self._filter_project(records)

        if entity == 'user':
            result = list(filter(is_user, records))

        if entity == 'slice':
            result = list(filter(is_silce, records))

        return result

    def _get_entity(self, hrn, entity):
        if entity in ['authority', 'project']:
            records = self._proxy.List(hrn, self.user_credential,
                                       {'recursive': True})
            list_data = getattr(self, "_filter_" + entity)(records)
        else:
            list_data = self._proxy.Resolve(hrn, self.user_credential,
                                            {})

        return list_data

    def _parse_authority(self, list_data):
        authorities = []
        for auth in list_data:
            if auth.get('hrn') is not None:

                upper_auth = '.'.join(auth.get('hrn').split('.')[:-1])

                new_auth = {
                    'id': auth.get('reg-urn'),
                    'shortname': auth.get('hrn').split('.')[-1],
                    'hrn': auth.get('hrn'),
                    'name': auth.get('name'),
                    'authority': hrn_to_urn(upper_auth, 'authority'),
                    'certificate': auth.get('gid'),
                    'created': self._datetime(auth['date_created']),
                    'updated': self._datetime(auth['last_updated']),
                    'pi_users': [hrn_to_urn(user, 'user') for user in auth.get('reg-pis', [])],
                    'users': auth.get('users', []),
                    'slices': auth.get('slices', []),
                    'projects': auth.get('projects', []),
                }

                authorities.append(new_auth)

        return authorities

    def _parse_project(self, list_data):
        projects = []
        for proj in list_data:
            # used to filter dorphan project
            if proj.get('hrn') is not None:

                upper_auth = '.'.join(proj.get('hrn').split('.')[:-1])

                new_proj = {
                        'id': proj.get('reg-urn'),
                        'shortname': proj.get('hrn').split('.')[-1],
                        'hrn': proj.get('hrn'),
                        'name': proj.get('name'),
                        'authority': hrn_to_urn(upper_auth, 'authority'),
                        'certificate': proj.get('gid'),
                        'created': self._datetime(proj['date_created']),
                        'updated': self._datetime(proj['last_updated']),
                        'pi_users': [hrn_to_urn(user, 'user') for user in proj.get('reg-pis', [])],
                        'users': proj.get('users', []),
                        'slices': proj.get('slices', []),
                    }
                projects.append(new_proj)

        return projects

    def _parse_user(self, list_data):
        users = []

        for user in list_data:
            new_user = {
                    'id':  user.get('reg-urn'),
                    'shortname': user['hrn'].split('.')[-1],
                    'hrn': user.get('hrn'),
                    'keys': user.get('reg-keys', []),
                    'certificate': user.get('gid'),
                    'email': user.get('email', ''),
                    'created': self._datetime(user['date_created']),
                    'updated': self._datetime(user['last_updated']),
                    'authority': hrn_to_urn(user['authority'], 'authority'),
                    'pi_authorities': [
                                        hrn_to_urn(pi_auth, 'authority')
                                        for pi_auth in user.get('reg-pi-authorities', [])
                                       ],
                    'projects': [
                                    hrn_to_urn(pi_auth, 'authority')
                                    for pi_auth in filter(
                                                          lambda x: len(x.split('.')) > 2,
                                                          user.get('reg-pi-authorities', [])
                                                          )
                                ],
                    'slices': [
                                hrn_to_urn(sli, 'slice') for sli in user.get('reg-slices', [])
                                ],

                }
            users.append(new_user)

        return users

    def _parse_slice(self, list_data):
        slices = []
        for sli in list_data:
            # users urn
            users = []
            geni_users = []
            for usr in sli.get('reg-researchers', []):
                usr_urn = hrn_to_urn(usr, 'user')
                users.append(usr_urn)
                usr_record = self._get_entity(usr, "user")
                geni_users.append({
                                    'urn': usr_urn,
                                    'keys': usr_record[0]['reg-keys'],
                                    'email': usr_record[0]['email']
                                })

            new_slice = {
                'id': sli.get('reg-urn'),
                'shortname': sli.get('hrn').split('.')[-1],
                'hrn': sli.get('hrn'),
                'created': self._datetime(sli['date_created']),
                'updated': self._datetime(sli['last_updated']),
                'users': users,
                'geni_users': geni_users,
                'authority': hrn_to_urn(sli['authority'], 'authority'),
                'project': hrn_to_urn('.'.join(sli['hrn'].split('.')[:-1]),
                                      'authority'),
            }

            slices.append(new_slice)

        return slices

    def get(self, entity, urn=None, raw=False):
        result = []
        try:
            if urn is None:
                result = self._get_entities(entity)
            else:
                hrn, type = urn_to_hrn(urn)
                if type not in self._types:
                    raise MysNotUrnFormatError('not valid urn')
                result = self._get_entity(hrn, entity)
            if not raw:
                result = getattr(self, '_parse_' + entity)(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.logs.append({
                                'endpoint': self.endpoint.name,
                                'url': self.endpoint.url,
                                'protocol': self.endpoint.protocol,
                                'type': self.endpoint.type,
                                'exception': str(e)
                            })
        return {'data': result, 'errors': self.logs}

    def get_credential(self, urn, delegated_to=None, raw=False):
        try:
            hrn, entity = urn_to_hrn(urn)

            if delegated_to:
                local_cred = list(filter(lambda c: c['id'] == urn and c['delegated_to']==delegated_to, self.user_credentials))
            else:
                local_cred = list(filter(lambda c: c['id'] == urn, self.user_credentials))

            if local_cred:
                cred = local_cred[0]['xml']
            else:
                if delegated_to:
                    # XXX To be removed
                    cred = self._proxy.GetCredential(self.user_credential, hrn, entity)
                    from sfa.trust.credential import Credential
                    from sfa.trust.gid import GID
                    credential = Credential(string=cred)
                    # TODO
                    # delegate(cred)
                    # use the private key of the user to sign the delegation of credentials
                    user_pkey = self.authentication.private_key
                    # gid of user
                    user = self._proxy.Resolve(self.authentication.hrn, self.user_credential, {})[0]
                    user_gid = GID(string=user['gid'], hrn=self.authentication.hrn)
                    # gid of the delegated_to user
                    delegate_user = self._proxy.Resolve(delegated_to, self.user_credential, {})[0]
                    delegate_gid = GID(string=delegate_user['gid'], hrn=delegated_to)
                    cred = self.delegate(credential, user_pkey, user_gid, delegate_gid)
                else:
                    cred = self._proxy.GetCredential(self.user_credential, hrn, entity)

            if raw:
                return cred

            d = [{
                'id': urn,
                'type': entity,
                'xml': cred, 
                'delegated_to': delegated_to,
            }]
            self.user_credentials += d

        except Exception as e:
            import traceback
            traceback.print_exc()
            d = []
            self.logs.append({
                                'endpoint': self.endpoint.name,
                                'url': self.endpoint.url,
                                'protocol': self.endpoint.protocol,
                                'type': self.endpoint.type,
                                'exception': str(e)
                            })
        return {'data':d,'errors':self.logs}

    def delegate(self, object_cred, private_key, from_gid, to_gid):
        pkey = None
        f_gid = None
        t_gid = None

        if isinstance(object_cred, str):
            if os.path.exists(object_cred):
                object_cred = Credential(filename=object_cred)
            else:
                object_cred = Credential(string=object_cred)

        if isinstance(private_key, str):
            if not os.path.exists(private_key):
                pkey = tempfile.NamedTemporaryFile(mode='w',delete=False)
                pkey.write(private_key)
                private_key = pkey.name
                pkey.close()

        if isinstance(from_gid, GID):
                from_gid = from_gid.save_to_string()
        if isinstance(from_gid, str):
            if not os.path.exists(from_gid):
                f_gid = tempfile.NamedTemporaryFile(mode='w',delete=False)
                f_gid.write(from_gid)
                from_gid = f_gid.name
                f_gid.close()

        if isinstance(to_gid, GID):
                to_gid = to_gid.save_to_string()
        if isinstance(to_gid, str):
            if not os.path.exists(to_gid):
                t_gid = tempfile.NamedTemporaryFile(mode='w',delete=False)
                t_gid.write(to_gid)
                to_gid = t_gid.name
                t_gid.close()

        dcred = object_cred.delegate(to_gid, private_key, from_gid)
        if pkey:
            os.unlink(pkey.name)
        if f_gid:
            os.unlink(f_gid.name)
        if t_gid:
            os.unlink(t_gid.name)
        return dcred.save_to_string(save_parents=True)

    # look up to see the upper has the credential
    def search_credential(self, hrn, entity):
        if entity == 'project':
            entity = 'authority'
        try:
            upper_hrn = '.'.join(hrn.split('.')[:-1])
            if hrn:
                if entity == 'slice':
                    # If credentials were provided don't call the Registry
                    c = self._getXmlCredential(hrn, entity)
                    if c: return c
                    #print('GetCredential hrn: '+hrn+' from Registry')
                    cred = self._proxy.GetCredential(self.user_credential, hrn, entity)
                    if cred:
                        return cred
                # If credentials were provided don't call the Registry
                c = self._getXmlCredential(upper_hrn, 'authority')
                if c: return c
                
                # if not upper_hrn or obj_type is None:
                #     upper_hrn = hrn
                
                #print('GetCredential upper: '+upper_hrn+' from Registry')
                return self._proxy.GetCredential(self.user_credential, upper_hrn, entity)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
            #import traceback
            #traceback.print_exc()
            return self.search_credential(upper_hrn, 'authority')

    def _user_mappings(self, hrn, record_dict):
        mapped_dict = {
                    'hrn': hrn,
                    'type': 'user',                 
                    'email': record_dict.get('email', ''), # email cant be empty string                  
                    'keys' : record_dict.get('keys', '')
        }

        # filter key have empty value
        mapped_dict = {k: v for k, v in mapped_dict.items() if v}
        return mapped_dict

    def _project_mappings(self, hrn, record_dict):
        return self._authority_mappings(hrn, record_dict)

    def _authority_mappings(self, hrn, record_dict):
        mapped_dict = {
                    'hrn': hrn,
                    'type': 'authority',                 
                    'name': record_dict.get('name', None),
                    'reg-pis': [urn_to_hrn(user)[0] for user in record_dict.get('pi_users', [])],
        }

        # filter key have empty value
        mapped_dict = {k: v for k, v in mapped_dict.items() if v}
        return mapped_dict

    def _slice_mappings(self, hrn, record_dict):

        mapped_dict = {
                    'hrn': hrn,
                    'type': 'slice',          
                    'reg-researchers': [urn_to_hrn(user)[0] for user in record_dict.get('users', [])],
        }

        # filter key have empty value
        mapped_dict = {k: v for k, v in mapped_dict.items() if v}
        return mapped_dict

    def create(self, entity, urn, record_dict):
        try:
            hrn = urn_to_hrn(urn)[0]
            auth_cred = self.search_credential(hrn, 'authority')
            if auth_cred:
                mapped_dict = getattr(self, '_'+entity+'_mappings')(hrn, record_dict)
                res = self._proxy.Register(mapped_dict, auth_cred)
                # XXX test the result either 1 or a gid
                res = self.get(entity, urn)
                result = res['data']
                self.logs += res['errors']
            else:
                raise SfaError('No Authority Credential for %s' % hrn)
        except Exception as e:
            result = []
            self.logs.append({
                                'endpoint': self.endpoint.name,
                                'url': self.endpoint.url,
                                'protocol': self.endpoint.protocol,
                                'type': self.endpoint.type,
                                'exception': str(e)
                            })
        return {'data':result,'errors':self.logs}

    def update(self, entity, urn, record_dict):
        result = []
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
                res = self._proxy.Update(mapped_dict, cred)
                # XXX test the result either 1 or a gid
                res = self.get(entity, urn)
                result = res['data']
                self.logs += res['errors']
            else:
                raise Exception("No Credential to update this Or Urn is Not Right", urn)
        except Exception as e:
            self.logs.append({
                                'endpoint': self.endpoint.name,
                                'url': self.endpoint.url,
                                'protocol': self.endpoint.protocol,
                                'type': self.endpoint.type,
                                'exception': str(e)
                            })
        
        return {'data':result,'errors':self.logs}

    def delete(self, entity, urn):
        result = []
        if entity == 'project':
            entity = 'authority'
        try:
            hrn = urn_to_hrn(urn)[0]
            auth_cred = self.search_credential(hrn, 'authority')
            if entity == 'authority':
                # Remove everything under it
                #print('remove everything under %s' % urn)
                pass
            if auth_cred:
                res = self._proxy.Remove(hrn, auth_cred, entity)
                if res != 1:
                    raise Exception(res)
        except Exception as e:
            self.logs.append({
                                'endpoint': self.endpoint.name,
                                'url': self.endpoint.url,
                                'protocol': self.endpoint.protocol,
                                'type': self.endpoint.type,
                                'exception': str(e)
                            })
        
        return {'data':result,'errors':self.logs}

    # self.CreateGid
