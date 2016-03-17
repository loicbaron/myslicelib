from myslicelib.util.sfabuilder import SfaBuilder

class Ple(SfaBuilder):

    def builder(self, urn, record_dict):
        result = []
        from pprint import pprint
        print(record_dict)
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
                'technologies':['Virtual Machines','Distributed Systems','Internet','Wired'],
            }

            #    'sliver_types': [
            #        {
            #        'name':'plab-vserver',
            #        'disk_images':[
            #            {
            #            'name':'Fedora 22',
            #            'os':'Linux',
            #            'version':'22',
            #            'description':'',
            #            #'url':'',
            #            }
            #        ]
            #        }
            #    ],

            for element in list(node):
                if 'hardware_type' in element.tag:
                    resource['hardware_types'].append(element.attrib['name'])
                if 'location' in element.tag:
                    resource['location'] = element.attrib
                    if not 'country' in resource['location'] or resource['location']['country']=='unknown' or resource['location']['country']==None:
                        resource['location']['country'] = self.get_planetlab_attribute(node,'country')

                if 'interface' in element.tag:
                    resource['interfaces'].append(element.attrib['component_id'])
                if 'available' in element.tag:
                    resource['available'] = element.attrib['now']

                if 'sliver_type' in element.tag:
                    resource['sliver_types'].append({'name':element.attrib['name'],'disk_images':[{
                        'name':'Fedora '+ self.get_planetlab_attribute(node, 'fcdistro'),
                        'os':'Linux',
                        'version':self.get_planetlab_attribute(node, 'fcdistro')
                    }]})
            result.append(resource)
        return result

    def get_planetlab_attribute(self, node, name):
        elements = node.findall('{http://www.planet-lab.org/resources/sfa/ext/planetlab/1}attribute')
        for el in elements:
            if el.attrib['name']==name:
                return el.attrib['value']


#  <node component_manager_id="urn:publicid:IDN+ple+authority+cm" component_id="urn:publicid:IDN+ple:uitple+node+planetlab1.cs.uit.no" exclusive="false" component_name="planetlab1.cs.uit.no">
#    <hardware_type name="plab-pc"/>
#    <hardware_type name="pc"/>
#    <location country="unknown" longitude="18.977" latitude="69.6813"/>
#    <interface component_id="urn:publicid:IDN+ple+interface+node14873:eth0" client_id="14873:466"/>
#    <available now="true"/>
#    <sliver_type name="plab-vserver">
#      <planetlab:initscript name="ple_sirius"/>
#      <planetlab:initscript name="ple_tophat"/>
#      <planetlab:initscript name="resa_demo"/>
#    </sliver_type>
#    <planetlab:attribute name="ccnindex" value="1"/>
#    <planetlab:attribute name="arch" value="x86_64"/>
#    <planetlab:attribute name="pldistro" value="lxc"/>
#    <planetlab:attribute name="fcdistro" value="f22"/>
#    <planetlab:attribute name="memy" value="5"/>
#    <planetlab:attribute name="responsey" value="1.0"/>
#    <planetlab:attribute name="reliabilitym" value="0"/>
#    <planetlab:attribute name="hrn" value="ple.uitple.planetlab1\.cs\.uit\.no"/>
#    <planetlab:attribute name="loadm" value="n/a"/>
#    <planetlab:attribute name="slicesm" value="n/a"/>
#    <planetlab:attribute name="memw" value="n/a"/>
#    <planetlab:attribute name="cpuy" value="0"/>
#    <planetlab:attribute name="slicesy" value="0"/>
#    <planetlab:attribute name="bww" value="n/a"/>
#    <planetlab:attribute name="country" value="Norway"/>
#    <planetlab:attribute name="cpum" value="n/a"/>
#    <planetlab:attribute name="memm" value="n/a"/>
#    <planetlab:attribute name="responsem" value="n/a"/>
#    <planetlab:attribute name="reliabilityw" value="0"/>
#    <planetlab:attribute name="slicesw" value="n/a"/>
#    <planetlab:attribute name="cpuw" value="n/a"/>
#    <planetlab:attribute name="bwm" value="n/a"/>
#    <planetlab:attribute name="loadw" value="n/a"/>
#    <planetlab:attribute name="asnumber" value="224"/>
#    <planetlab:attribute name="responsew" value="n/a"/>
#    <planetlab:attribute name="region" value="Troms"/>
#    <planetlab:attribute name="reliability" value="0"/>
#    <planetlab:attribute name="load" value="n/a"/>
#    <planetlab:attribute name="cpu" value="n/a"/>
#    <planetlab:attribute name="mem" value="n/a"/>
#    <planetlab:attribute name="bw" value="n/a"/>
#    <planetlab:attribute name="response" value="n/a"/>
#    <planetlab:attribute name="reliabilityy" value="19"/>
#    <planetlab:attribute name="loady" value="1.0"/>
#    <planetlab:attribute name="slices" value="n/a"/>
#    <planetlab:attribute name="bwy" value="25.6"/>
#    <planetlab:attribute name="inccn" value="yes"/>
#  </node>

