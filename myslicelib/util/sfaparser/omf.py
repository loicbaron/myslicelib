
def parser(rspec, entity=None):
    result = []
    el = rspec.find('{http://www.geni.net/resources/rspec/3}node')
    testbed = el.attrib['component_id'].split("+")[1]
    if ':' in testbed:
        testbed = testbed.split(":")[1]

    if entity == 'lease':
        # XXX TODO parse leases
        #for lease in rspec.findall('{http://nitlab.inf.uth.gr/schema/sfa/rspec/1}lease'):
        return result

    else:
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
                'technologies':['Wireless','Wifi'],
            }
            for element in list(node):
                if 'location' in element.tag:
                    resource['location'] = element.attrib
            result.append(resource)
    return result
