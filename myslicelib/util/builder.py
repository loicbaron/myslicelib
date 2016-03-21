from copy import deepcopy
import xml.etree.ElementTree
from myslicelib.util.parser import get_testbed_type

class Builder(object):

    _options = {
        'geni_rspec_version' : {'type': 'GENI', 'version': '3'}
    }

    def __init__(self, parser, testbed):
        self.parser = parser   
        self.testbed = testbed
    
    def build(self, urn, record_dict):
        try:
            builder_module = __import__("myslicelib.util.sfabuilder." + self.parser, fromlist=[''])
            class_ = getattr(builder_module, self.parser.title())
            instance_ = class_()
           
            record = deepcopy(record_dict)
            # Filter resources matching the AM
            record['resources'] = list(filter(lambda x: x['manager'].startswith('+'.join(self.testbed.split('+')[:2])), record['resources']))
            if 'leases' in record:
                for l in record['leases']:
                    # Filter resources in leases matching the AM
                    l['resources'] = list(filter(lambda x: x.startswith('+'.join(self.testbed.split('+')[:2])), l['resources']))
                    # If the AM is not concerned by this lease, delete it from the list
                    if len(l['resources'])==0:
                        record['leases'].remove(l) 
                    
            return getattr(instance_, 'builder')(urn, record)
        except Exception as e:
            raise NotImplementedError("Parser not implemented")

