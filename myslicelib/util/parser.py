import xml.etree.ElementTree

class Parser(object):

    _options = {
        'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
    }

    _rspec_ams = {
        'omf' : ['nitos','omf','omf.nitos','omf.netmode','netmode','gaia','omf.gaia','snu','omf.snu','omf.kaist','r2lab','omf.r2lab','faraday','omf.faraday','omf.etri'],
        'iotlab' : ['iotlab','iii'],                    # IoT
        'ple' : ['ple'],                                # PlanetLab
        'fuseco' : ['fuseco.fokus.fraunhofer.de'],
        'emulab' : ['wilab2.ilabt.iminds.be'],          # iMinds
        'openflow' : ['openflow','ofam','ofelia'],      # Ofelia Openflow
        'virtualization' : ['virtualization','vtam']    # Ofelia VM
    }

    def __init__(self, xml_rspec, options=None):
        if not options:
            self.options = self._options
        else:
            self.options = options

        self.rspec = xml.etree.ElementTree.fromstring(xml_rspec)

        el = self.rspec.find('{http://www.geni.net/resources/rspec/3}node')
        self.rspec_am = el.attrib['component_id'].split("+")[1].split(":")[0]

    def parse(self, entity):
        parser = None
        for rs in self._rspec_ams:
            if (self.rspec_am in self._rspec_ams[rs]):
                parser = rs
                break    

        if (parser):            
            parser_module = __import__("myslicelib.util.sfaparser." + parser, fromlist=[''])
            class_ = getattr(parser_module, parser.title())
            instance_ = class_()
            return getattr(instance_, entity + '_parser')(self.rspec)
        else:
            raise NotImplementedError("Parser not implemented")