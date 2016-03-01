from myslicelib.util.sfaparser import SfaParser

class Fuseco(SfaParser):

    def resource_parser(self, rspec):

        result = []

        for node in rspec.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {
            'type' : 'node',
            'id': node.attrib['component_id'],
            'hostname': node.attrib['component_name'],
            }
            for element in list(node):
                if 'location' in element.tag:
                    resource['location'] = element.attrib
                    result.append(resource)
                    return result