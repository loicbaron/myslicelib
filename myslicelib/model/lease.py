from myslicelib.model import Entities, Entity

class Leases(Entities):
    pass

class Lease(Entity):
    _class = "Lease"
    _type = "lease"
    _collection = "Leases"

    _generator = ['start_time', 'end_time', 'duration']

    def __init__(self, data = {}):
        super().__init__(data)
        if data is None:
            data = {}
        self.resources = data.get('resources', [])

    def addResource(self, resource):
        self.appendAttribute('resources', resource.id)
        return self

    def addResources(self, resources):
        for r in resources:
            self.addResource(r)
        return self

    def removeResource(self, resource):
        self.setAttribute('resources', list(set(self.resources) - set([resource.id])))
        return self

    def removeResources(self):
        self.resources = [] 
        return self

    def setStartTime(self, value):
        self.setAttribute('start_time', value)
        if 'duration' in self._attributes:
            self.setAttribute('end_time', self.start_time + self.duration)
        if 'end_time' in self._attributes:
            self.setAttribute('duration', self.end_time - self.start_time)

    def setEndTime(self, value):
        self.setAttribute('end_time', value)
        if 'duration' in self._attributes:
            self.setAttribute('start_time', self.end_time - self.duration)
        if 'start_time' in self._attributes:
            self.setAttribute('duration', self.end_time - self.start_time)

    def setDuration(self, value):
        self.setAttribute('duration', value)
        if 'start_time' in self._attributes:
            self.setAttribute('end_time', self.start_time + self.duration)
        if 'end_time' in self._attributes:
            self.setAttribute('start_time', self.end_time - self.duration)

    def get_end_time(self, start_time, duration):
        return start_time + duration
    def get_start_time(self, end_time, duration):
        return end_time - duration
    def get_duration(self, start_time, end_time):
        return end_time - start_time

    def save(self, setup=None):
        raise NotImplemented("A Lease has to be part of a slice to be saved slice.save()")

    def delete(self, setup=None):
        raise NotImplemented("A Lease has to be part of a slice to be removed slice.removeLease()")

    def update(self):
        raise NotImplemented("A Lease has to be part of a slice to be updated slice.addLease()")

