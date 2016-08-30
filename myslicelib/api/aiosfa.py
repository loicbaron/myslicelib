import ssl
import os.path
import asyncio

from urllib.parse import urlparse

from myslicelib import setup as s
from myslicelib.util import Endpoint, Authentication
from myslicelib.api.aioclient import ServerProxy


class Sfa(object):

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
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                # We have no way of loading a chain from string buffer,
                # let's do a temp file.
                # https://docs.python.org/3/library/tempfile.html
                with tempfile.NamedTemporaryFile(mode='w',
                                                 delete=False) as cert_fn:
                    with tempfile.NamedTemporaryFile(mode='w',
                                                     delete=False) as pkey_fn:
                        cert_fn.write(self.authentication.certificate)
                        pkey_fn.write(self.authentication.private_key)

                        context.load_cert_chain(
                                cert_fn.name,
                                keyfile=pkey_fn.name,
                                password=None
                        )

        except ssl.SSLError as e:
            exit("Problem with certificate and/or key")

        except Exception as e:
            # import traceback
            # traceback.print_exc()
            exit("Problem Authenticating with certificate and/or key")

        self._proxy = ServerProxy(self.endpoint.url, allow_none=True,
                                  verbose=False, use_datetime=True,
                                  context=context)

    async def version(self, raw=False):
        try:
            result = await self._proxy.GetVersion()
            self._proxy.close()
            # XXX Cope with the difference between AM & Registry responses
            if 'value' in result:
                result = result['value']
            else:
                result['geni_api'] = result['sfa']

            if raw:
                return result

            return {
                    'data': [{
                        'status': {
                            'online': True,
                            'message': None
                        },
                        'id': result['urn'],
                        'version': result['geni_api'],
                        'type': self.endpoint.type,
                        'url': self.endpoint.url,
                        'hostname': urlparse(self.endpoint.url).hostname,
                        'name': self.endpoint.name,
                        'api': {
                            "type": self.endpoint.type,
                            "protocol": self.endpoint.protocol,
                            'version': result['geni_api'],
                        },
                    }],
                    'errors': [],
                }
        except Exception as e:
            return {
                    'data': [{
                        'status': {
                            'online': False,
                            'message': e
                        },
                        'id': None,
                        'version': None,
                        'type': None,
                        'url': self.endpoint.url,
                        'hostname': urlparse(self.endpoint.url).hostname,
                        'name': self.endpoint.name,
                        'api': {
                            "type": self.endpoint.type,
                            "protocol": self.endpoint.protocol,
                            "version": None,
                        },
                    }],
                    'errors': [e],
                }

if __name__ == '__main__':

    path = "/var/myslice/"
    pkey = path + "myslice.pkey"
    hrn = "onelab.myslice"
    email = "support@myslice.info"
    cert = path + "myslice.cert"

    s.authentication = Authentication(hrn=hrn, email=email,
                                      certificate=cert, private_key=pkey)

    endpoint = Endpoint(url="https://localhost:6080", type="Reg")
    authentication = Authentication(hrn=hrn, email=email,
                                    certificate=cert, private_key=pkey)

    instance = Sfa(endpoint=endpoint, authentication=authentication)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(instance.version())
    loop.stop()
