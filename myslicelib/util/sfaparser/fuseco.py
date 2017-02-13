from myslicelib.util.sfaparser import SfaParser

class Fuseco(SfaParser):

    def resource_parser(self, rspec, source):

        result = []

        for node in rspec.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {
            'type' : 'node',
            'id': node.attrib['component_id'],
            'name': node.attrib['component_name'],
            'manager': node.attrib['component_manager_id'],
            'testbed': source,
            'services': [],
            'parser':self.__class__.__name__.lower(),
            }
            for element in list(node):
                if 'location' in element.tag:
                    resource['location'] = element.attrib
                    result.append(resource)
                    return result
