from models import Model
from fields import StringField, DateField, IntegerField, BooleanField
from MongoDBMixins import MongoDBFieldMix
from decorators.storage_decorators import stored

from datetime import date

@stored(backend="AppEngine")
class FileModel(Model):
    """ A simple file model.
    
    This model inherits directly from a supplied mixin - in this case, one that
    enables the model to talk to Google's AppEngine database.
    
    If your backend changes, the only code you need to change for this model is
    the the decorator argument - instead of "AppEngine", put "MongoDB" 
    (for example), or whatever is appropriate for your backend.
    """
    
    name = StringField
    size = IntegerField
    filetype = StringField
    notes = StringField
    created = DateField
    is_safe = BooleanField
    
    def my_size(self):
        """ A function specific to this model, unmanaged by QUI """
        return u"{} bytes".format(self.size)
    
    def __init__(self):
        self.size = 100
        

class FMSub(FileModel):
    purple = BooleanField
    _host = "google.com"
    
    def __init__(self):
        super(FMSub, self).__init__(self)
        self.purple = False
