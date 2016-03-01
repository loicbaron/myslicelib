class SfaParser(object):

    def resource_parser(self, rspec):
        return []

    def slice_parser(self, rspec):
        return [{'resources':self.resource_parser(rspec), 'leases':self.lease_parser(rspec)}]

    def lease_parser(self, rspec):
        return []
