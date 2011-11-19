from models import *
from fields import *
from modelmixins import *
from fieldmixins import *


class StrField(MDBFieldMix, StringField):
    pass

class IntField(MDBFieldMix, IntegerField):
    pass

class TestModel(MDBModelMix, Model):
    def __init__(self, *args, **kwargs):
        super(TestModel,self).__init__(*args, **kwargs)
        self.name = StrField()
        self.age = IntField(primary_key=True)