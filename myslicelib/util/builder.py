import xml.etree.ElementTree

class Builder(object):

    _options = {
        'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
    }

    def __init__(self, testbed):
        self.testbed = testbed    
    
    def build(self, urn, record_dict):
            if self.testbed is not None:            
                builder_module = __import__("myslicelib.util.sfabuilder." + self.testbed, fromlist=[''])
                class_ = getattr(builder_module, self.testbed.title())
                instance_ = class_()
                return getattr(instance_, 'builder')(urn, record_dict)
            else:
                raise NotImplementedError("Parser not implemented")

