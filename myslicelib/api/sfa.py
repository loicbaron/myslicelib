from xmlrpc import client as xmlrpcclient
import ssl

class Api(object):

    def __init__(self, endpoint=None, credential=None):
        self.endpoint = endpoint
        self.credential = credential

        self.type_ams = {
            'omf' : ['nitos','omf','omf.nitos','omf.netmode','netmode','gaia','omf.gaia','snu','omf.snu','omf.kaist','r2lab','omf.r2lab','faraday','omf.faraday','omf.etri'],
            'iotlab' : ['iotlab','iii'],                    # IoT
            'ple' : ['ple'],                                # PlanetLab
            'fuseco' : ['fuseco.fokus.fraunhofer.de'],
            'emulab' : ['wilab2.ilabt.iminds.be'],          # iMinds
            'openflow' : ['openflow','ofam','ofelia'],      # Ofelia Openflow
            'virtualization' : ['virtualization','vtam']    # Ofelia VM
        }


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

        self._proxy = xmlrpcclient.ServerProxy(self.endpoint.url, allow_none=True, verbose=False, use_datetime=True, context=context)

        # version call
        self._version = self._version()

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
                for t in self.type_ams:
                    if result['value']['urn'].split("+")[1].split(":")[0] in self.type_ams[t]:
                        testbed = t
                        continue
                return {
                    'status': {
                        'online' : True,
                        'message' : None
                    },
                    'id': result['value']['urn'],
                    'version' : result['value']['geni_api'],
                    'testbed' : testbed,
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


