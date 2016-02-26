
def parser(rspec):
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
            'exclusive': node.attrib['exclusive'],
            'hardware_types': [],
            'interfaces': [],
            'sliver_types': [],
            'testbed':testbed,
            'technologies':['IoT','Internet of Things'],
        }
        for element in list(node):
            if 'hardware_type' in element.tag:
                resource['hardware_types'].append(element.attrib['name'])

            if 'location' in element.tag:
                resource['location'] = element.attrib

            if 'available' in element.tag:
                resource['available'] = element.attrib['now']

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
