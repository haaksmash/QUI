from models import Model
from fields import StringField, DateField, IntegerField, BooleanField
from decorators.storage_decorators import stored, subclass
from decorators.field_decorators import class_field

#Some horrible jankery to get AppEngine to look in the correct directories
import os, sys
from os.path import dirname, basename, splitext, join 
GOOGLE_PATH = "C:/Program Files (x86)/Google/google_appengine" 
EXTRA_PATHS = [
    GOOGLE_PATH, 
    os.path.join(GOOGLE_PATH, 'lib', 'django'), 
    os.path.join(GOOGLE_PATH, 'lib', 'webob'), 
    os.path.join(GOOGLE_PATH, 'lib', 'yaml', 'lib'), 
] 
for directory in EXTRA_PATHS: 
    if not directory in sys.path: 
        sys.path.insert(0, directory) 
        
import AppEngineMixins

@stored(backend="AppEngine")
class FileModel(Model):
    """ A simple file model.
    
    This model inherits directly from a supplied mixin - in this case, one that
    enables the model to talk to Google's AppEngine database.
    
    If your backend changes, the only code you need to change for this model is
    the the decorator argument - instead of "AppEngine", put "MongoDB" 
    (for example), or whatever is appropriate for your backend.
    """
    
    sys.path.append("C:/Program Files (x86)/Google/google_appengine")
    
        
    count = class_field(IntegerField)
    
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
        FileModel.count += 1
        self.size = 100
        
    def __unicode__(self):
        if self.name:
            return u"{}".format(self.name)
        else:
            return u"{}".format("Unnamed File")
        
@subclass
class FMSub(FileModel):
    purple = BooleanField
    _host = "google.com"
    
    #count = class_field(IntegerField)
    
    def __init__(self):
        super(FMSub, self).__init__(self)
        FMSub.count += 1
        self.purple = False
