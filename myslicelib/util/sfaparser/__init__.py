class SfaParser(object):

    def resource_parser(self, rspec, source):
        return []

    def slice_parser(self, rspec, source):
        return [{'resources':self.resource_parser(rspec, source), 'leases':self.lease_parser(rspec, source)}]

    def lease_parser(self, rspec, source):
        return []
