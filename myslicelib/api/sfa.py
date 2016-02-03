import xmlrpclib
import ssl
from httplib import HTTPSConnection

from myslicelib.util.certificate import Keypair, Certificate

###
# ServerException, ExceptionUnmarshaller
#
# Used to convert server exception strings back to an exception.
#    from usenet, Raghuram Devarakonda

class ServerException(Exception):
    pass

class ExceptionUnmarshaller(xmlrpclib.Unmarshaller):

    def close(self):
        try:
            return xmlrpclib.Unmarshaller.close(self)
        except xmlrpclib.Fault, e:
            raise ServerException(e.faultString)


class XMLRPCTransport(xmlrpclib.Transport):

    def __init__(self, key_file=None, cert_file=None, timeout=None):
        xmlrpclib.Transport.__init__(self)
        self.timeout = timeout
        self.key_file = key_file
        self.cert_file = cert_file

    def make_connection(self, host):
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        host, extra_headers, x509 = self.get_host_info(host)

        # Using a self signed certificate
        # https://www.python.org/dev/peps/pep-0476/
        if hasattr(ssl, '_create_unverified_context'):
            conn = HTTPSConnection(host, None, key_file=self.key_file, cert_file=self.cert_file,
                               context=ssl._create_unverified_context())
        else:
            conn = HTTPSConnection(host, None, key_file=self.key_file, cert_file=self.cert_file)

        # Some logic to deal with timeouts. It appears that some (or all) versions
        # of python don't set the timeout after the socket is created. We'll do it
        # ourselves by forcing the connection to connect, finding the socket, and
        # calling settimeout() on it. (tested with python 2.6)
        if self.timeout:
            if hasattr(conn, 'set_timeout'):
                conn.set_timeout(self.timeout)

            if hasattr(conn, "_conn"):
                # HTTPS is a wrapper around HTTPSConnection
                real_conn = conn._conn
            else:
                real_conn = conn

            conn.connect()

            if hasattr(real_conn, "sock") and hasattr(real_conn.sock, "settimeout"):
                real_conn.sock.settimeout(float(self.timeout))

        return conn

    def getparser(self):
        unmarshaller = ExceptionUnmarshaller()
        parser = xmlrpclib.ExpatParser(unmarshaller)
        return parser, unmarshaller

class XMLRPCServerProxy(xmlrpclib.ServerProxy):

    def __init__(self, url, transport, allow_none=True, verbose=False):
        self.url = url
        xmlrpclib.ServerProxy.__init__(self, url, transport, allow_none=allow_none, verbose=verbose)


    def __getattr__(self, attr):
        return xmlrpclib.ServerProxy.__getattr__(self, attr)

class Api(object):

    def __init__(self, url, pkey, email=None, hrn=None, certfile=None, verbose=False, timeout=None):
        self.url = url

        if not certfile:
            certfile = self.sign_certificate(pkey, email, hrn) #
        else:
            certfile = certfile
         
        self.verbose = verbose
        self.timeout = timeout

        transport = XMLRPCTransport(pkey, certfile, timeout)
        self.serverproxy = XMLRPCServerProxy(url, transport, allow_none=True, verbose=verbose)

    def __getattr__(self, name):

        def func(*args, **kwds):
            return getattr(self.serverproxy, name)(*args, **kwds)

        return func
    
    def version(self):
        try:
            result = self.GetVersion()
        except Exception, e:
            print e
            return False
        return result


