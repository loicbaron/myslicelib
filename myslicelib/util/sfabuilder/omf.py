import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from pprint import pprint
from myslicelib.api.sfa import SfaError
from myslicelib.util.sfabuilder import SfaBuilder

NEW_LEASE_TAG = '<ol:lease client_id="%(client_id)s" valid_from="%(valid_from_iso)sZ" valid_until="%(valid_until_iso)sZ"/>'
OLD_LEASE_TAG = '<ol:lease id="%(lease_id)s" valid_from="%(valid_from_iso)sZ" valid_until="%(valid_until_iso)sZ"/>'
LEASE_REF_TAG = '<ol:lease_ref id_ref="%(lease_id)s"/>'
NODE_TAG = '<node component_id="%(urn)s">' 
# component_manager_id="urn:publicid:IDN+omf:xxx+authority+am" component_name="node1" exclusive="true" client_id="my_node">'
NODE_TAG_END = '</node>'
CHANNEL_TAG = '<ol:channel component_id="%(urn)s">'
CHANNEL_TAG_END = '</ol:channel>'

# XXX Not tested:
LINK_TAG = '<link component_id="%(urn)s">'
LINK_TAG_END = '</link>'

class Omf(SfaBuilder):

    @classmethod
    def builder(cls, urn, record_dict):
        rspec = []
        cls.rspec_add_header(rspec)
        if 'resources' not in record_dict:
            raise SfaError('Resources must be specified')
        if 'leases' not in record_dict:
            raise SfaError('Leases must be specified to reserve resources')
        lease_map = cls.rspec_add_leases(rspec, record_dict['leases'])
        cls.rspec_add_resources(rspec, record_dict['resources'], lease_map)
        cls.rspec_add_footer(rspec)
        pprint(rspec)
        return "\n".join(rspec)

    @classmethod
    def rspec_add_header(cls, rspec):
        rspec.append("""<?xml version="1.0"?>
<rspec type="request" xmlns="http://www.geni.net/resources/rspec/3" xmlns:ol="http://nitlab.inf.uth.gr/schema/sfa/rspec/1" xmlns:omf="http://schema.mytestbed.net/sfa/rspec/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd http://nitlab.inf.uth.gr/schema/sfa/rspec/1 http://nitlab.inf.uth.gr/schema/sfa/rspec/1/request-reservation.xsd">""")

    @classmethod
    def rspec_add_footer(cls, rspec):
        rspec.append('</rspec>')

    @classmethod
    def rspec_add_leases(cls, rspec, leases):
        # A map (resource key) -> [ { client_id: UUID, lease_id: ID_or_None }, ... ]
        lease_map = {}

        # A map (interval) -> (lease_id) to group reservations by interval == 1 RSPEC LEASE
        map_interval_lease_id = {}

        pprint(leases)
        for lease in leases:
            interval = (lease['start_time'], lease['end_time'])
            if not interval in map_interval_lease_id:
                map_interval_lease_id[interval] = {'lease_id': None, 'client_id': str(uuid.uuid4()) }
            lease_id = lease.get('lease_id', None)
            if lease_id:
                # If grouped, all leases will have the same ID, so we can update it each time
                map_interval_lease_id[interval]['lease_id'] = lease_id

            pprint(lease_map)
            for r in lease['resources']:
                if not r in lease_map:
                    lease_map[r] = list()
                lease_map[r].append(map_interval_lease_id[interval])
                
        for (valid_from, valid_until), lease_dict in map_interval_lease_id.items():
            valid_from_iso = datetime.utcfromtimestamp(int(valid_from)).isoformat()
            valid_until_iso = datetime.utcfromtimestamp(int(valid_until)).isoformat()

            # NITOS Broker not supporting timezones
            #valid_from_iso = "%s%+02d:%02d" %  ((datetime.utcfromtimestamp(int(valid_from))  + timedelta(hours=3)).isoformat(), 3, 00)
            #valid_until_iso = "%s%+02d:%02d" % ((datetime.utcfromtimestamp(int(valid_until)) + timedelta(hours=3)).isoformat(), 3, 00)

            lease_id = lease_dict['lease_id']
            client_id = lease_dict['client_id']

            if lease_id:
                rspec.append(OLD_LEASE_TAG % locals())
            else:
                rspec.append(NEW_LEASE_TAG % locals())

        return lease_map

    @classmethod
    def rspec_add_resources(cls, rspec, resources, lease_map):
        pprint(resources)
        for resource in resources:
            urn = resource['id']
            type = resource['type'] 

            resource = {
                'urn'           : urn,
                'type'          : type,
            }
            # What information do we need in resources for REQUEST ?
            resource_type = resource.pop('type')

            # We add lease_ref wrt to each lease_id (old leases) and each client_id (new leases)
            lease_dicts = lease_map.get(resource['urn'])

            # NOTE : Shall we ignore reservation of resources without leases ?
            lease_ids = list()
            if lease_dicts:
                for lease_dict in lease_dicts:
                    lease_id = lease_dict.get('lease_id')
                    if not lease_id:
                        lease_id = lease_dict.get('client_id')
                    lease_ids.append(lease_id)

            print(resource_type)

            if resource_type == 'node':
                cls.rspec_add_node(rspec, resource, lease_ids)
            elif resource_type == 'link':
                cls.rspec_add_link(rspec, resource, lease_ids)
            elif resource_type == 'channel':
                cls.rspec_add_channel(rspec, resource, lease_ids)

    @classmethod
    def rspec_add_lease_ref(cls, rspec, lease_id):
        if lease_id:
            rspec.append(LEASE_REF_TAG % locals())

    @classmethod
    def rspec_add_node(cls, rspec, node, lease_ids):
        rspec.append(NODE_TAG % node)
        for lease_id in lease_ids:
            cls.rspec_add_lease_ref(rspec, lease_id)
        rspec.append(NODE_TAG_END)

    @classmethod
    def rspec_add_channel(cls, rspec, channel, lease_ids):
        rspec.append(CHANNEL_TAG % channel)
        for lease_id in lease_ids:
            cls.rspec_add_lease_ref(rspec, lease_id)
        rspec.append(CHANNEL_TAG_END)

    @classmethod
    def rspec_add_link(cls, rspec, link, lease_ids):
        rspec.append(LINK_TAG % link)
        for lease_id in lease_ids:
            cls.rspec_add_lease_ref(rspec, lease_id)
        rspec.append(LINK_TAG_END)
