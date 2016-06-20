from urllib.parse import urlparse
import socket

from myslicelib.model import Entity, Entities

class Testbed(Entity):
    _class = "Testbed"
    _type = "testbed"
    _collection = "Testbeds"

    @property
    def ip(self):
        return socket.gethostbyname(self.hostname)

class Testbeds(Entities):
    pass
