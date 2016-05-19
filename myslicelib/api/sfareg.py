import os, tempfile
import pytz
import traceback

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
                    print(c['id'] +': is expired')

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
        # attept to list the hrn first if it is an authority
        # if hrn is not an authority, it will list all elements
        return self._proxy.List(hrn, self.user_credential, {'recursive':True})

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
            geni_users = []
            for r in d.get('reg-researchers', []):
                u = self._user(self._get_entity(r))
                geni_users.append({'urn':u[0]['id'],'keys':u[0]['keys'],'email':u[0]['email']})
                users.append(hrn_to_urn(r, 'user'))

            slices.append({
                'id' : d.get('reg-urn'),
                'shortname': d.get('hrn').split('.')[-1],
                'hrn': d.get('hrn'),
                'created': self._datetime(d['date_created']),
                'updated': self._datetime(d['last_updated']),
                'users': users,
                'geni_users': geni_users,
                'authority': hrn_to_urn(d['authority'], 'authority'),
                'project': hrn_to_urn('.'.join(d['hrn'].split('.')[:-1]), 'authority'),
            })
        return slices

    #def _authority(self, data):
    #    authority = []
    #    for d in data:

    #        mappings = {
    #            'slice': [],
    #            'user': [],
    #            'authority': [],
    #        }
    #        ### XXX need optimatiztion with query(id = None)
    #        enitities = self._extract_with_authority(d['hrn'], self._list_entity(d['hrn']))

    #        for entity in enitities:
    #            # depend object tpye, we add this object urn to its coresponding mappings
    #            mappings[entity['type']] += [entity['reg-urn']]

    #        authority.append({
    #            'id': d.get('reg-urn'),
    #            'shortname': d.get('hrn').split('.')[-1],
    #            'hrn': d.get('hrn'),
    #            'name': d.get('name'),
    #            'authority': hrn_to_urn('.'.join(d.get('hrn').split('.')[:-1]), 'authority'),
    #            'certificate': d.get('gid'),
    #            'created': self._datetime(d['date_created']),
    #            'updated': self._datetime(d['last_updated']),
    #            'pi_users': [hrn_to_urn(user, 'user') for user in d.get('reg-pis', [])],
    #            'users': mappings['user'],
    #            'slices': mappings['slice'],
    #            'projects': mappings['authority']
    #        })
    #    return authority

    def analyze_authorities(self, data):
        from collections import defaultdict
        l_authorities = defaultdict(dict)
        for d in data:
            if d.get('classtype')=='authority': 
                a = d.get('hrn')
                if a is None or len(a.split('.')) < 3:
                    if d.get('hrn') in l_authorities.keys():
                        l_authorities[d.get('hrn')].update(d)
                    else:
                        l_authorities[d.get('hrn')] = d
                else:
                    if 'project' in l_authorities[d.get('authority')]:
                        l_authorities[d.get('authority')]['project'].append(d.get('reg-urn'))
                    else:
                        l_authorities[d.get('authority')]['project']=[d.get('reg-urn')]
               
            else:
                if d.get('classtype') in l_authorities[d.get('authority')]:
                    l_authorities[d.get('authority')][d.get('classtype')].append(d.get('reg-urn'))
                else:
                    l_authorities[d.get('authority')][d.get('classtype')]=[d.get('reg-urn')]
        return l_authorities


    def _authority(self, data):
        authority = []
        l_authorities = self.analyze_authorities(data)
        mappings = {
            'slice': [],
            'user': [],
            'authority': [],
        }

        ### XXX need optimatiztion with query(id = None)
        #enitities = self._extract_with_authority(d['hrn'], self._list_entity(d['hrn']))
        for d in l_authorities.values():
            # depend object tpye, we add this object urn to its coresponding mappings
            #mappings[entity['type']] += [entity['reg-urn']]

            # Avoid Orphan element
            # XXX This should not happen: when we delete an element, we should delete everything uder it!!!
            if d.get('hrn') is not None:
                authority.append({
                    'id': d.get('reg-urn'),
                    'shortname': d.get('hrn').split('.')[-1],
                    'hrn': d.get('hrn'),
                    'name': d.get('name'),
                    'authority': hrn_to_urn('.'.join(d.get('hrn').split('.')[:-1]), 'authority'),
                    'certificate': d.get('gid'),
                    'created': self._datetime(d['date_created']),
                    'updated': self._datetime(d['last_updated']),
                    'pi_users': [hrn_to_urn(user, 'user') for user in d.get('reg-pis', [])],
                    'users': d.get('user',[]),
                    'slices': d.get('slice',[]),
                    'projects': d.get('project',[]),
                })
            #else:
            #    print("WARNING: Authority Orphan element found, clean up the registry %s" % d)
        return authority

    def analyze_projects(self, data):
        from collections import defaultdict
        l_projects = defaultdict(dict)
        for d in data:
            o = d.get('hrn')
            a = d.get('authority')
            if d.get('classtype')=='authority': 
                if o is not None and len(o.split('.')) > 2:
                    if d.get('hrn') in l_projects.keys():
                        l_projects[d.get('hrn')].update(d)
                    else:
                        l_projects[d.get('hrn')] = d
            elif a is not None and len(a.split('.')) > 2:
                if d.get('classtype') in l_projects[d.get('authority')]:
                    l_projects[d.get('authority')][d.get('classtype')].append(d.get('reg-urn'))
                else:
                    l_projects[d.get('authority')][d.get('classtype')]=[d.get('reg-urn')]
        return l_projects


    def _project(self, data):
        project = []
        mappings = {
            'slice': [],
            'user': [],
        }
        l_projects = self.analyze_projects(data)
        for d in l_projects.values():
            # Avoid Orphan element
            # XXX This should not happen: when we delete an element, we should delete everything uder it!!!
            if d.get('hrn') is not None:
                project.append({
                    'id' :  d.get('reg-urn'),
                    'shortname': d.get('hrn').split('.')[-1],
                    'hrn': d.get('hrn'),
                    'name': d.get('name'),
                    'authority': hrn_to_urn('.'.join(d.get('hrn').split('.')[:-1]), 'authority'),
                    'certificate': d.get('gid'),
                    'created': self._datetime(d['date_created']),
                    'updated': self._datetime(d['last_updated']),
                    'pi_users': [hrn_to_urn(user, 'user') for user in d.get('reg-pis', [])],
                    'users': d.get('user',[]),
                    'slices': d.get('slice',[]),
                })
            else:
                print("WARNING: Projec Orphan element found, clean up the registry %s" % d)

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
        try:
            if urn is None:
                if entity == 'authority' or entity == 'project':
                    result = self._list_entity()
                else:
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

                if entity == 'authority' or entity == 'project':
                    result = self._list_entity(hrn)
                else:
                    result = self._get_entity(hrn)

            if raw:
                result = self._extract_with_entity(entity, result)
            else:
                result = getattr(self, "_" + entity)(result)
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

    def get_credential(self, urn, delegated_to=None, raw=False):
        hrn, entity = urn_to_hrn(urn)

        if delegated_to:
            local_cred = list(filter(lambda c: c['id'] == urn and c['delegated_to']==delegated_to, self.user_credentials))
        else:
            local_cred = list(filter(lambda c: c['id'] == urn, self.user_credentials))

        if local_cred:
            print('already defined %s' % urn)
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
                    print('GetCredential hrn: '+hrn+' from Registry')
                    cred = self._proxy.GetCredential(self.user_credential, hrn, entity)
                    if cred:
                        return cred
                # If credentials were provided don't call the Registry
                c = self._getXmlCredential(upper_hrn, 'authority')
                if c: return c
                
                # if not upper_hrn or obj_type is None:
                #     upper_hrn = hrn
                
                print('GetCredential upper: '+upper_hrn+' from Registry')
                return self._proxy.GetCredential(self.user_credential, upper_hrn, entity)
            return False
        except Exception as e:
            # if Error, go to upper level until reach the root level
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
            traceback.print_exc()

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
            traceback.print_exc()
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
                print('remove everything under %s' % urn)
            if auth_cred:
                res = self._proxy.Remove(hrn, auth_cred, entity)
                if res != 1:
                    raise Exception(res)
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

    # self.CreateGid
