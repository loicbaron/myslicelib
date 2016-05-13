from myslicelib.model import Entities, Entity

class Leases(Entities):
    pass

class Lease(Entity):
    _class = "Lease"
    _type = "lease"
    _collection = "Leases"

    _generator = ['start_time', 'end_time', 'duration']

    def __init__(self, data = None):
        super().__init__(data)
        if data is None:
            self.resources = []

    def addResource(self, resource):
        self.resources.append(resource.id)
        return self

    def addResources(self, resources):
        for r in resources:
            self.addResource(r)
        return self

    def removeResource(self, resource):
        self.resources = list(set(self.resources) - set([resource.id]))
        return self

    def removeResources(self):
        self.resources = [] 
        return self

    def _generate_with_start_time(self):
        if 'duration' in self._attributes:
            group = dict(
                start_time = self.start_time,
                duration = self.duration,
                end_time = self.start_time + self.duration
            )
            return group
        if 'end_time' in self._attributes:
            group = dict(
                start_time = self.start_time,
                duration = self.end_time - self.start_time,
                end_time = self.end_time
            )
            return group
        return {}

    def _generate_with_end_time(self):
        if 'duration' in self._attributes:
            group = dict(
                start_time = self.end_time - self.duration,
                duration = self.duration,
                end_time = self.end_time
            )
            return group
        if 'start_time' in self._attributes:
            group = dict(
                start_time = self.start_time,
                duration = self.end_time - self.start_time,
                end_time = self.end_time
            )
            return group
        return {}

    def _generate_with_duration(self):
        if 'start_time' in self._attributes:
            group = dict(
                start_time = self.start_time,
                duration = self.duration,
                end_time = self.start_time + self.duration
            )
            return group
        if 'end_time' in self._attributes:
            group = dict(
                start_time = self.end_time - self.duration,
                duration = self.duration,
                end_time = self.end_time
            )
            return group
        return {}

    def get_end_time(self, start_time, duration):
        return start_time + duration
    def get_start_time(self, end_time, duration):
        return end_time - duration
    def get_duration(self, start_time, end_time):
        return end_time - start_time

    def save(self):
        raise NotImplemented("A Lease has to be part of a slice to be saved slice.save()")

    def delete(self):
        raise NotImplemented("A Lease has to be part of a slice to be removed slice.removeLease()")

    def update(self):
        raise NotImplemented("A Lease has to be part of a slice to be updated slice.addLease()")

