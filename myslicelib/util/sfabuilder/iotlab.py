import xml.etree.ElementTree as ET
from myslicelib.api.sfa import SfaError
from myslicelib.util.sfabuilder import SfaBuilder

class Iotlab(SfaBuilder):

    def builder(self, urn, record_dict):
        #<?xml version="1.0"?>
        #  <rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xmlns:plos="http://www.planet-lab.org/resources/sfa/ext/plos/1" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="request" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://www.planet-lab.org/resources/sfa/ext/planetlab/1 http://www.planet-lab.org/resources/sfa/ext/planetlab/1/planetlab.xsd http://www.planet-lab.org/resources/sfa/ext/plos/1 http://www.planet-lab.org/resources/sfa/ext/plos/1/plos.xsd" expires="2014-05-30T17:07:46Z" generated="2014-05-30T16:07:46Z">
        #    <node component_manager_id="urn:publicid:IDN+iotlab+authority+cm" component_id="urn:publicid:IDN+iotlab+node+a8-144.devgrenoble.iot-lab.info" component_name="a8-144.devgrenoble.iot-lab.info">
        #      <sliver_type name="iotlab-node"/>
        #    </node>
        #    <node component_manager_id="urn:publicid:IDN+iotlab+authority+cm" component_id="urn:publicid:IDN+iotlab+node+m3-35.devstras.iot-lab.info" component_name="m3-35.devstras.iot-lab.info">
        #      <sliver_type name="iotlab-node"/>
        #    </node>
        #    <lease slice_id="urn:publicid:IDN+ple:upmc+slice+myslicedemo" start_time="1402005600" duration="420">
        #      <node component_id="urn:publicid:IDN+iotlab+node+m3-35.devstras.iot-lab.info"/>
        #      <node component_id="urn:publicid:IDN+iotlab+node+a8-144.devgrenoble.iot-lab.info"/>
        #    </lease>
        #  </rspec>

        rspec = '<?xml version="1.0"?><rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xmlns:plos="http://www.planet-lab.org/resources/sfa/ext/plos/1" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="request" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://www.planet-lab.org/resources/sfa/ext/planetlab/1 http://www.planet-lab.org/resources/sfa/ext/planetlab/1/planetlab.xsd http://www.planet-lab.org/resources/sfa/ext/plos/1 http://www.planet-lab.org/resources/sfa/ext/plos/1/plos.xsd" expires="2014-05-30T17:07:46Z" generated="2014-05-30T16:07:46Z">'

        for r in record_dict['resources']:
            rspec += '<node component_manager_id="'+r['manager']+'" component_id="'+r['id']+'" component_name="'+r['id'].split('+')[-1]+'">'
            rspec += '<sliver_type name="iotlab-node"/>'
            rspec += '</node>'

        if 'leases' not in record_dict:
            raise SfaError('Leases must be specified to reserve FIT IoT-LAB resources')

        for l in record_dict['leases']:
            rspec += '<lease slice_id="'+urn+'" start_time="'+str(l['start_time'])+'" duration="'+str(int(l['duration']/60))+'">'
            for r in l['resources']:
                rspec += '<node component_id="'+r+'"/>'
            rspec += '</lease>'

        rspec += '</rspec>'
        print(rspec)
        return rspec
