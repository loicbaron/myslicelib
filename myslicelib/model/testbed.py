from urllib.parse import urlparse
import socket

from myslicelib.model import Entity, Entities

class Testbed(Entity):
    _name = "Testbed"

    @property
    def hostname(self):
        return urlparse(self.api_url).hostname

    @property
    def ip(self):
        return socket.gethostbyname(self.hostname)

class Testbeds(Entities):
    pass