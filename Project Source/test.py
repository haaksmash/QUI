from models import Model
from fields import *
from decorators import stored

@stored()
class MongoModel(Model):
    _backend = "mongodb"

class FileModel(MongoModel):
    count = 0
    
    def to_readable(self):
        return u"{}".format(self.size)
    
    def __init__(self):
        super(FileModel, self).__init__()
        FileModel.count += 1

class MongoLocal(MongoModel):
    _port = 27018
     
class LocalFile(MongoLocal):
    pass

    
@stored(backend="mongodb", host="labrain.st.hmc.edu")
class OtherMongo(Model):
    pass

class TestModel(OtherMongo):
    pass
