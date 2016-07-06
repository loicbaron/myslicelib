import random
import string
import myslicelib

from myslicelib import setup as s, Setup
from myslicelib.api import Api

from myslicelib.model import Entities, Entity
from myslicelib.query import q

from myslicelib.util.sfa import urn_to_hrn


class Users(Entities):
    pass

class User(Entity):
    _class = "User"
    _type = "user"
    _collection = "Users"
    credentials = []
   
    def getAuthority(self, attribute=False):
        if attribute:
            return self.getAttribute('authority')
        else:
            Authority = myslicelib.model.authority.Authority
            urn = self.getAttribute('authority')
            return q(Authority).id(urn).get()

    def getPiAuthorities(self, attribute=False):
        if attribute:
            return self.getAttribute('pi_authorities')
        else:
            Authority = myslicelib.model.authority.Authority
            pi_auths = self.getAttribute('pi_authorities')
            # TODO parallel requests using MultiProcess
            result = []
            for urn in pi_auths:
                result += q(Authority).id(urn).get()
            return result

    def getSlices(self, attribute=False):
        if attribute:
            return self.getAttribute('slices')
        else:
            Slice = myslicelib.model.slice.Slice
            result = []
            for urn in self.getAttribute('slices'):
                result += q(Slice).id(urn).get()
            return result

    def getCredential(self, id, delegate_to=None, setup=None, attribute=False):
        return self.getCredentials(id, delegate_to, setup)

    def getCredentials(self, id=None, delegate_to=None, setup=None, attribute=False):
        if attribute:
            return self.getAttribute('credentials')
        else:
            try:
                if setup and isinstance(setup, Setup):
                    _setup = setup
                else:
                    _setup = s

                if id:
                    ids = [id]
                else:
                    ids =[]
                    ids.append(self.getAttribute('id'))

                    for urn in self.getAttribute('slices'):
                        ids.append(urn)

                    for urn in self.getAttribute('pi_authorities'):
                        ids.append(urn)

                res = self._api(_setup).get_credentials(ids, delegate_to)
                self.setAttribute('credentials', res['data'])
                self.logs = res['errors']
            except Exception as e:
                #import traceback
                #traceback.print_exc()
                raise Exception('Failed to fetch the Credentials')

        return self

    ##
    # HRN
    def generateHrn(self):
        a = self.email.split('@')[0].replace(".", "_").replace("+", "_")
        b = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(4))
        return a + b

    # User hrn can be set also from his email
    def getHrn(self):
        if not self.hasAttribute('hrn'):
            if self.hasAttribute('email') and self.hasAttribute('authority'):
                self.setAttribute('hrn',
                                    '.'.join([
                                        urn_to_hrn(self.authority)[0],
                                        self.generateHrn()
                                    ])
                                  )
            if not self.hasAttribute('shortname'):
                self.setAttribute('shortname', self.getAttribute('hrn').split('.')[-1])

        return self.getAttribute('hrn')

    def save(self, setup=None):
        # check if we have the email
        if not self.hasAttribute('email'):
            raise Exception('User email must be specified')

        if not self.hasAttribute('authority'):
            raise Exception('Authority for the user must be specified')

        return super().save()
