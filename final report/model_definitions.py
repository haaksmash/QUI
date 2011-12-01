from qui.models import Model
from qui.decorators.storage import stored

from my_package.other_models import Host, User

stored(backend="AppEngine")
class File(Model):
    """ A simple file model.
    
    This model inherits directly from a supplied mixin - in this case, one that
    enables the model to talk to Google's AppEngine database.
    
    If your backend changes, the only code you need to change for this model is
    the the decorator argument - instead of "AppEngine", put "MongoDB" (for example), or whatever 
    is appropriate for your backend.
    """
    
    """
    Notice that fields attributes are declared _uninitialized_; this is by design.
    You won't be able to declare
        name = StringField()
    because by itself, the StringField class doesn't satisfy all of its abstract members.
    QUI does magic in the background to give each field the required attributes, so that they
    can talk to the backends properly.
    """
    name = StringField
    size = IntegerField
    type = StringField  # by default, StringFields are limited 
                        # to 256 characters. You can limit this
                        # further by specifying the max_length
                        # argument.
    notes = StringField
    created = DateField
    
    def my_size(self):
        """ A function specific to this model, unmanaged by QUI """
        return u"{} bytes".format(self.size)
        
    # If you intend to instantiate any File objects, the next two lines are required:
    def __init__(self, *args, **kwargs): # (you need not specify *args or **kwargs, though)
        super(File, self).__init__()
        # anything after this line is up to you, but nothing else is needed.
        