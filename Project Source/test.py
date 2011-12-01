from models import Model
from fields import StringField, DateField, IntegerField, BooleanField
from MongoDBMixins import MongoDBFieldMix
from decorators.storage_decorators import stored

from datetime import date

class StrField(MongoDBFieldMix, StringField):
    pass


@stored(backend='test')
class MongoModel(Model):
    pass

class FileModel(MongoModel):
    count = 0
    
    name = StringField
    path = StringField
    dateadded = DateField
    size = IntegerField
    genre = StringField
    
    safe = BooleanField
    
    def to_readable(self):
        return self.size
    
    def __init__(self, path=None, date=None, size=None):
        super(FileModel, self).__init__()
        FileModel.count += 1
        self.size = size
        self.path = path
        self.date = date


class MongoLocal(MongoModel):
    _port = 27018
     
class LocalFile(MongoLocal):
    pass

    
@stored(backend="AppEngine")
class AEModel(Model):
    pass

class TestModel(AEModel):
    name = StringField

    def __init__(self):
        super(TestModel, self).__init__()
        
        
        
x = FileModel()
print x.to_readable()
        