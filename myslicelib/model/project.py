import myslicelib

from myslicelib.model.authority import Authorities, Authority
from myslicelib.query import q

class Projects(Authorities):
    pass

class Project(Authority):
    _class = "Project"
    _type = "Authority"
    _collection = "Projects"
