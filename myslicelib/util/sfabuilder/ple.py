import xml.etree.ElementTree as ET
from myslicelib.util.sfabuilder import SfaBuilder

class Ple(SfaBuilder):

    def builder(self, urn, record_dict):
        result = []
        from pprint import pprint
        print(record_dict)

        #<?xml version="1.0"?>
        #  <rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xmlns:plos="http://www.planet-lab.org/resources/sfa/ext/plos/1" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="request" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://www.planet-lab.org/resources/sfa/ext/planetlab/1 http://www.planet-lab.org/resources/sfa/ext/planetlab/1/planetlab.xsd http://www.planet-lab.org/resources/sfa/ext/plos/1 http://www.planet-lab.org/resources/sfa/ext/plos/1/plos.xsd" expires="2016-03-18T12:26:50Z" generated="2016-03-18T11:26:50Z">
        #    <node component_manager_id="urn:publicid:IDN+ple+authority+cm" component_id="urn:publicid:IDN+ple:urvple+node+planetlab1.urv.cat" component_name="planetlab1.urv.cat">
        #      <sliver_type name="plab-vserver"/>
        #    </node>
        #    <node component_manager_id="urn:publicid:IDN+ple+authority+cm" component_id="urn:publicid:IDN+ple:irisaple+node+inriarennes2.irisa.fr" component_name="inriarennes2.irisa.fr">
        #      <sliver_type name="plab-vserver"/>
        #    </node>
        #  </rspec>
        rspec = '<?xml version="1.0"?>\
        <rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xmlns:plos="http://www.planet-lab.org/resources/sfa/ext/plos/1" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="request" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://www.planet-lab.org/resources/sfa/ext/planetlab/1 http://www.planet-lab.org/resources/sfa/ext/planetlab/1/planetlab.xsd http://www.planet-lab.org/resources/sfa/ext/plos/1 http://www.planet-lab.org/resources/sfa/ext/plos/1/plos.xsd" expires="2016-03-18T12:26:50Z" generated="2016-03-18T11:26:50Z">'

        for r in record_dict['resources']:
            rspec += '<node component_manager_id="urn:publicid:IDN+ple+authority+cm" component_id="'+r['id']+'" component_name="'+r['id'].split('+')[-1]+'">'
            rspec += '<sliver_type name="plab-vserver"/>'
            rspec += '</node>'

        rspec += '</rspec>'

        return rspec

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

