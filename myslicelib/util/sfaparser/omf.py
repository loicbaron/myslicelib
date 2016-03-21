import dateutil.parser
from myslicelib.util.sfaparser import SfaParser

class Omf(SfaParser):

    def lease_parser(self, rspec):
        result = []
        el = rspec.find('{http://www.geni.net/resources/rspec/3}node')

        leases = rspec.findall('{http://nitlab.inf.uth.gr/schema/sfa/rspec/1}lease')

        if not leases:
            return result

        nodes = rspec.findall('{http://www.geni.net/resources/rspec/3}node')    
        for lease in leases:
            dt = dateutil.parser.parse(lease.attrib['valid_from'])
            start_time = int(dt.strftime("%s"))
            dt = dateutil.parser.parse(lease.attrib['valid_until'])
            end_time = int(dt.strftime("%s"))
            duration = end_time - start_time
            l = {            
                'lease_id': lease.attrib['id'],
                'parser':self.__class__.__name__.lower(),
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration,
                'resources': [],
            }        
            for node in nodes:
                leases_in_node = node.findall('{http://nitlab.inf.uth.gr/schema/sfa/rspec/1}lease_ref')
                if not leases_in_node:
                    continue
                else:
                    for lease_in_node in leases_in_node:
                        if l['lease_id'] == lease_in_node.attrib['id_ref']:
                            l['resources'].append(node.attrib['component_id'])
            result.append(l)
        return result

    def resource_parser(self, rspec):
        result = []
        el = rspec.find('{http://www.geni.net/resources/rspec/3}node')

        for node in rspec.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {
                'type' : 'node',
                'id': node.attrib['component_id'],
                'name': node.attrib['component_name'],
                'manager': node.attrib['component_manager_id'],
                'parser':self.__class__.__name__.lower(),
                'exclusive': node.attrib['exclusive'],
                'hardware_types': [],
                'interfaces': [],
                'sliver_types': [],
                'parser':self.__class__.__name__.lower(),
                'technologies':['Wireless','Wifi'],
            }
            for element in list(node):
                if 'location' in element.tag:
                    resource['location'] = element.attrib
            result.append(resource)

            # TODO channel?
        return result

# node

#  'component_id="urn:publicid:IDN+omf:paris.fit-nitos.fr+interface+node41:if1" '
#  'component_name="node41:if1" role="experimental"/>\n'
#  '  </node>\n'
# channel

#  '  <ol:channel '
#  'component_id="urn:publicid:IDN+omf:paris.fit-nitos.fr+channel+channel1" '
#  'component_manager_id="urn:publicid:IDN+omf:paris.fit-nitos.fr+authority+cm" '
#  'component_name="channel1" frequency="2.412GHz"/>\n'
