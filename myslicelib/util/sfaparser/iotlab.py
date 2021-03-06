from myslicelib.util.sfaparser import SfaParser

class Iotlab(SfaParser):

    def lease_parser(self, rspec, source):
        result = []
        el = rspec.find('{http://www.geni.net/resources/rspec/3}node')

        for lease in rspec.findall('{http://www.geni.net/resources/rspec/3}lease'):
            lease = {
                'slice_id': lease.attrib['slice_id'],
                'start_time': int(lease.attrib['start_time']),
                'duration': int(lease.attrib['duration'])*60,
                'end_time': int(lease.attrib['start_time']) + \
                            int(lease.attrib['duration'])*60,

                'resources': [node.attrib['component_id'] for node in list(lease)],
                'testbed': source,
                'parser':self.__class__.__name__.lower(),
            }
            result.append(lease)
        return result


    def resource_parser(self, rspec, source):
        result = []
        el = rspec.find('{http://www.geni.net/resources/rspec/3}node')

        for node in rspec.findall('{http://www.geni.net/resources/rspec/3}node'):
            resource = {
                'type' : 'node',
                'id': node.attrib['component_id'],
                'name': node.attrib['component_name'],
                'manager': node.attrib['component_manager_id'],
                'testbed': source,
                'exclusive': node.attrib['exclusive'],
                'hardware_types': [],
                'interfaces': [],
                'sliver_types': [],
                'services': [],
                'parser':self.__class__.__name__.lower(),
                'technologies':['IoT','Internet of Things'],
            }
            for element in list(node):
                if 'hardware_type' in element.tag:
                    resource['hardware_types'].append(element.attrib['name'])

                if 'location' in element.tag:
                    resource['location'] = element.attrib
                    resource['location']['city'] = node.attrib['component_name'].split('.')[1].title()

                if 'available' in element.tag:
                    resource['available'] = element.attrib['now']

                if 'services' in element.tag:
                    login = element.find('{http://www.geni.net/resources/rspec/3}login')
                    resource['services'].append({'login':login.attrib})

            result.append(resource)
        return result

#  <node component_manager_id="urn:publicid:IDN+iotlab+authority+sa" component_id="urn:publicid:IDN+iotlab+node+m3-83.lille.iot-lab.info" exclusive="true" component_name="m3-83.lille.iot-lab.info">
#    <hardware_type name="m3:at86rf231"/>
#    <location country="France"/>
#    <granularity grain="30"/>
#    <available now="true"/>
#    <sliver_type name="plab-vserver"/>
#  </node>
#  <lease slice_id="urn:publicid:IDN+iotlab+slice+amdouni_slice" start_time="1454491946" duration="50000">
#    <node component_id="urn:publicid:IDN+iotlab+node+a8-3.rocquencourt.iot-lab.info"/>
#    <node component_id="urn:publicid:IDN+iotlab+node+a8-5.rocquencourt.iot-lab.info"/>
#    <node component_id="urn:publicid:IDN+iotlab+node+a8-7.rocquencourt.iot-lab.info"/>
#  </lease>
