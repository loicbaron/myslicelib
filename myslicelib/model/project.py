import myslicelib

from myslicelib.model import Entities, Entity
from myslicelib.query import q

class Projects(Entities):
    pass

class Project(Entity):
    _class = "Project"
    _collection = "Projects"

