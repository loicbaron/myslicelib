import xmlrpc.client as xmlrpc
import ssl
from http.client import HTTPSConnection

from xmlrpc import client as xmlrpcclient
import ssl
from http.client import HTTPSConnection
from myslicelib.util import Endpoint, Credential

# class XMLRPCTransport(object):
#
#     def __init__(self, credential):
#         xmlrpc.client.Transport.__init__(self)
#         #self.timeout = timeout
#         self.key_file = credential.pkey
#         self.cert_file = credential.certificate
#
#     def make_connection(self, host):
#         # create a HTTPS connection object from a host descriptor
#         # host may be a string, or a (host, x509-dict) tuple
#         host, extra_headers, x509 = self.get_host_info(host)
#
#         # Using a self signed certificate
#         # https://www.python.org/dev/peps/pep-0476/
#         if hasattr(ssl, '_create_unverified_context'):
#             conn = HTTPSConnection(host, None, key_file=self.key_file, cert_file=self.cert_file,
#                                context=ssl._create_unverified_context())
#         else:
#             conn = HTTPSConnection(host, None, key_file=self.key_file, cert_file=self.cert_file)
#
#         return conn

class Api(object):

    def __init__(self, endpoint: Endpoint, credential: Credential) -> None:
        self.endpoint = endpoint
        self.credential = credential

        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        else:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        try:
            context.load_cert_chain(
                    self.credential.sign_certificate(),
                    keyfile=self.credential.private_key,
                    password=None
            )

        except ssl.SSLError as e:
            exit("Problem with certificate and/or key")

        self.proxy = xmlrpcclient.ServerProxy(self.endpoint.url, allow_none=True, verbose=False, context=context)


    def version(self):
        try:
            result = self.proxy.GetVersion()
        except Exception as e:
            print(e)
            return False
        return result


class SfaError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


