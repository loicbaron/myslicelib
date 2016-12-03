import ssl
import socket
import os.path
import sys, tempfile, time
from urllib.parse import urlparse
from myslicelib.util.sfa import hrn_to_urn

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
                #print(pkey_fn.name)
                #print(cert_fn.name)
                context.load_cert_chain(
                        cert_fn.name,
                        keyfile=pkey_fn.name,
                        password=None
                )
                os.unlink(cert_fn.name)
                os.unlink(pkey_fn.name)
        except ssl.SSLError as e:
            import traceback
            traceback.print_exc()
            raise Exception("Problem with certificate and/or key")

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception("Problem Authenticating with certificate and/or key")

        # DEFAULT TIMEOUT is set in Endpoint
        socket.setdefaulttimeout(self.endpoint.timeout)

        self._proxy = xmlrpcclient.ServerProxy(self.endpoint.url, allow_none=True, verbose=False, use_datetime=True, context=context)

        # version call
        self._version = self.version(raw=True)

        # logs
        self.logs = []

    def version(self, raw=False):
        message = None
        version = None
        urn = None
        ret = {}
        online = False
        status = "offline"

        try:
            ret = self._proxy.GetVersion()
            if 'value' in ret:
                # AM
                version = ret['value']['geni_api']
                if 'urn' in ret['value']:
                    urn = ret['value']['urn']
                else:
                    urn = hrn_to_urn(ret['value']['hrn'], 'authority')
                online = True
                status = "online"
            elif 'sfa' in ret:
                # Registry
                version = ret['sfa']
                urn = ret['urn']
                online = True
                status = "online"
            else:
                message = "Error parsing returned value"

        except socket.timeout:
            message = "Connection timed out ({})".format(self.endpoint.url)

        except socket.gaierror:
            message = "Server name/address not provided or unknown ({})".format(self.endpoint.url)

        except Exception as e:
            message = str(e)

        if raw:
            if 'value' in ret:
                return ret['value']
            return ret
        else:
            return {
                'data': [{
                    'status': status,
                    "connection":{
                        'online' : online,
                        'message' : message
                    },
                    'id': urn,
                    'version': version,
                    'type': self.endpoint.type,
                    'url' : self.endpoint.url,
                    'technologies' : self.endpoint.technologies,
                    'hostname' : urlparse(self.endpoint.url).hostname,
                    'name' : self.endpoint.name,
                    'api' : {
                        "type" : self.endpoint.type,
                        "protocol" : self.endpoint.protocol,
                        'version': version,
                    },
                }],
                'errors':[message],
            }


class SfaError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


