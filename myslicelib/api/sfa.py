import ssl
import socket

from xmlrpc import client as xmlrpcclient

class Api(object):

    def __init__(self, endpoint=None, authentication=None):
        self.endpoint = endpoint
        self.authentication = authentication

        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        else:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        try:
            context.load_cert_chain(
                    self.authentication.certificate,
                    keyfile=self.authentication.private_key,
                    password=None
            )

        except ssl.SSLError as e:
            exit("Problem with certificate and/or key")

        self._proxy = xmlrpcclient.ServerProxy(self.endpoint.url, allow_none=True, verbose=False, use_datetime=True, context=context)
        # DEFAULT TIMEOUT is set in Endpoint
        socket.setdefaulttimeout(self.endpoint.timeout)
        # version call
        self._version = self._version()

        # logs
        self.logs = []

    def version(self):
        return self._version

    def _version(self):
        try:
            result = self._proxy.GetVersion()
            if 'interface' in result and result['interface'] == 'registry':
                return {
                    'status': {
                        'online' : True,
                        'message' : None
                    },
                    'id': result['urn'],
                    'version': result['sfa'],
                    'type': 'registry'
                }
            else :
                return {
                    'status': {
                        'online' : True,
                        'message' : None
                    },
                    'id': result['value']['urn'],
                    'version' : result['value']['geni_api'],
                    'type' : 'am'
                }
        except Exception as e:
            return {
                'status': {
                    'online' : False,
                    'message' : e
                },
                'id': None,
                'version' : None,
                'type' : None
            }


class SfaError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


