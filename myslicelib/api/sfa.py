from xmlrpc import client as xmlrpcclient
import ssl

class Api(object):

    def __init__(self, endpoint=None, credential=None):
        self.endpoint = endpoint
        self.credential = credential

        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        else:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        try:
            context.load_cert_chain(
                    self.credential.certificate,
                    keyfile=self.credential.private_key,
                    password=None
            )

        except ssl.SSLError as e:
            exit("Problem with certificate and/or key")

        self._proxy = xmlrpcclient.ServerProxy(self.endpoint.url, allow_none=True, verbose=False, context=context)

        # version call
        self._version = self.version()

    def version(self):
        try:
            result = self._proxy.GetVersion()
            if 'interface' in result and result['interface'] == 'registry':
                return {
                    'hostname': result['hostname'],
                    'id': result['urn'],
                    'version': result['sfa'],
                    'type': 'registry',
                    'backend': ''
                }
            else :
                return {
                    'hostname': result['value']['hostname'],
                    'id': result['value']['urn'],
                    'version' : result['value']['geni_api'],
                    'type' : 'am',
                    'backend' : result['value']['testbed']
                }
        except Exception as e:
            return { 'hostname': '', 'id': '', 'version' : '', 'type' : '','backend' : '' }


class SfaError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


