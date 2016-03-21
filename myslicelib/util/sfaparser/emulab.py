from myslicelib.util.sfaparser import SfaParser

class Emulab(SfaParser):

    def resource_parser(self, rspec):
        result = []
        el = rspec.find('{http://www.geni.net/resources/rspec/3}node')
        testbed = el.attrib['component_id'].split("+")[1]
        if ':' in testbed:
            testbed = testbed.split(":")[1]

        for node in rspec.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {
                'type' : 'node',
                'id': node.attrib['component_id'],
                'name': node.attrib['component_name'],
                'manager': node.attrib['component_manager_id'],
                'exclusive': node.attrib['exclusive'],
                'hardware_types': [],
                'interfaces': [],
                'sliver_types': [],
                'parser':self.__class__.__name__.lower(),

            }
            for element in list(node):
                if 'hardware_type' in element.tag:
                    resource['hardware_types'].append(element.attrib['name'])

                if 'location' in element.tag:
                    resource['location'] = element.attrib

                if 'interface' in element.tag:
                    resource['interfaces'].append(element.attrib['component_id'])
                if 'available' in element.tag:
                    resource['available'] = element.attrib['now']

                if 'sliver_type' in element.tag:
                    disk_images = list()
                    for e in list(element):
                        if 'disk_image' in e.tag:
                            disk_images.append(e.attrib) 
                    resource['sliver_types'].append(
                    {'name':element.attrib['name'],
                    'disk_images':disk_images}
                    )

            if 'wilab' in testbed:
                resource['technologies']=['Wireless', 'Wifi', 'IoT', 'Internet of Things', '802.15.4']
            if 'wall' in testbed:
                resource['technologies']=['Virtual Machines','Bare Metal','Internet','Wired']

            result.append(resource)
        return result
