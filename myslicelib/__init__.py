import xmlrpclib
import socket
import ssl


class Api(object):

    def __init__(self, auth=None, url=None):
        self.auth = auth
        self.url = url

        # Manifold uses a self signed certificate
        # https://www.python.org/dev/peps/pep-0476/
        if hasattr(ssl, '_create_unverified_context'):
            self.server = xmlrpclib.Server(self.url, verbose=False, allow_none=True,
                                                     context=ssl._create_unverified_context())
        else:
            self.server = xmlrpclib.Server(self.url, verbose=False, allow_none=True)

        try:
            self.server._()   # Call a fictive method.
        except xmlrpclib.Fault:
            # connected to the server and the method doesn't exist which is expected.
            print "fault"
            pass
        except socket.error:
            # Not connected ; socket error mean that the service is unreachable.
            print "sock"

        # Just in case the method is registered in the XmlRPC server
        print "ok"



'''
DEBUG MANIFOLD -> DICT :
{
    'timestamp': 'now',
    'object': 'local:platform',
    'params': {},
    'filters': [
        ['disabled', '==', '0'],
        ['platform', '!=', 'myslice'],
        ['gateway_type', '==', 'sfa']
    ],
    'fields': [
        'platform',
        'platform_longname',
        'platform_url',
        'gateway_type',
        'platform_description'
    ],
    'action': 'get'
}
'''
