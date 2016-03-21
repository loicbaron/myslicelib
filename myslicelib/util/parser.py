import xml.etree.ElementTree

type_ams = {
    'omf' : ['nitos','omf','omf.nitos','omf.netmode','netmode','gaia','omf.gaia','snu','omf.snu','omf.kaist','r2lab','omf.r2lab','faraday','omf.faraday','omf.etri'],
    'iotlab' : ['iotlab','iii'],                    # IoT
    'ple' : ['ple'],                                # PlanetLab
    'fuseco' : ['fuseco.fokus.fraunhofer.de'],
    'emulab' : ['wilab2.ilabt.iminds.be'],          # iMinds
    'openflow' : ['openflow','ofam','ofelia'],      # Ofelia Openflow
    'virtualization' : ['virtualization','vtam']    # Ofelia VM
}

def get_testbed_type(id):
    for t in type_ams:
        if id.split("+")[1].split(":")[0] in type_ams[t]:
            return t

class Parser(object):

    _options = {
        'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
    }

    def __init__(self, testbed, xml_rspec, options=None):
        if not options:
            self.options = self._options
        else:
            self.options = options

        self.testbed = testbed    
        self.rspec = xml.etree.ElementTree.fromstring(xml_rspec)

        el = self.rspec.find('{http://www.geni.net/resources/rspec/3}node')
        if el is not None:
            self.rspec_am = el.attrib['component_id'].split("+")[1].split(":")[0]
        else:
            self.rspec_am = None

    def parse(self, entity):
        try:
            parser_module = __import__("myslicelib.util.sfaparser." + self.testbed, fromlist=[''])
            class_ = getattr(parser_module, self.testbed.title())
            instance_ = class_()
            return getattr(instance_, entity + '_parser')(self.rspec)
        except Exception as e:
            raise NotImplementedError("Parser not implemented")
