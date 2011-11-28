from models import Model
from fields import *
from fieldmixins import *
from decorators import stored

class StrField(MDBFieldMix, StringField):
    pass

class IntField(MDBFieldMix, IntegerField):
    pass

@stored(db="mongodb")
class TestModel(Model):
    id = 12345
    name = StringField
    
    
class Tester2(object):
    id = 0

    def __init__(self):
        id = getattr(Tester2, "id")
        self.id = id
        setattr(Tester2, "id", id+1)