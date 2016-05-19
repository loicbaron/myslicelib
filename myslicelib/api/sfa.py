import ssl
import socket
import os.path
import sys, tempfile, time

from pprint import pprint

#from OpenSSL.crypto import FILETYPE_PEM, load_privatekey, load_certificate
#from OpenSSL.SSL import TLSv1_METHOD, Context, Connection, VERIFY_NONE

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
            if os.path.isfile(self.authentication.private_key):
                context.load_cert_chain(
                        self.authentication.certificate,
                        keyfile=self.authentication.private_key,
                        password=None
                )
            else:
                #context = Context(TLSv1_METHOD)
                #context.use_privatekey(load_privatekey(FILETYPE_PEM, self.authentication.private_key))
                #context.use_certificate(load_certificate(FILETYPE_PEM, self.authentication.certificate))
                #context.verify_mode = ssl.CERT_REQUIRED
                #context.check_hostname = False
                #sock = socket.create_connection((host, port), timeout=self.endpoint.timeout)
                # XXX OpenSSL.SSL.Context has no method wrap_socket
                # but xmlrpcclient.ServerProxy expects a context with wrap_socket method
                #context.wrap_socket(sock)

                # XXX ssl.SSLContext has a wrap_socket method, but it expects files for private_key and certificate
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                # We have no way of loading a chain from string buffer, let's do a temp file
                cert_fn = tempfile.NamedTemporaryFile(mode='w',delete=False)
                cert_fn.write(self.authentication.certificate)
                cert_fn.close()
                pkey_fn = tempfile.NamedTemporaryFile(mode='w',delete=False)
                pkey_fn.write(self.authentication.private_key)
                pkey_fn.close()
                context.load_cert_chain(
                        cert_fn.name,
                        keyfile=pkey_fn.name,
                        password=None
                )
                os.unlink(cert_fn.name)
                os.unlink(pkey_fn.name)
        except ssl.SSLError as e:
            exit("Problem with certificate and/or key")

        except Exception as e:
            import traceback
            traceback.print_exc()
            exit("Problem Authenticating with certificate and/or key")

        # DEFAULT TIMEOUT is set in Endpoint
        socket.setdefaulttimeout(self.endpoint.timeout)

        self._proxy = xmlrpcclient.ServerProxy(self.endpoint.url, allow_none=True, verbose=False, use_datetime=True, context=context)
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


