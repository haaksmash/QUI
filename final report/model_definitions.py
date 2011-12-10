from qui.models import Model
from qui.fields import *
from qui.decorators.storage import stored
from qui.decorators.field_decorators import class_field

@stored(backend="MongoDB")
class FileModel(Model):
    """ A simple file model.
    
    This model will inherit directly from a supplied mixin - in this case, one 
    that enables the model to talk to MongoDB.
    
    If your backend changes, the only code you need to change for this model is
    the the decorator argument - instead of "MongoDB", put "Pickle" 
    (for example), or whatever is appropriate for your backend.
    """
    
    count = class_field(IntegerField)

    name = StringField
    size = IntegerField
    filetype = StringField
    notes = StringField
    created = DateField
    is_safe = BooleanField
    
    class_var = 100
    
    def my_size(self):
        """ A function specific to this model, unmanaged by QUI """
        return u"{} bytes".format(self.size)
    
    def __unicode__(self):
        if self.name:
            return u"{}".format(self.name)
        else:
            return u"{}".format("Unnamed File")