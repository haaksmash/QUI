from qui.models import *

from my_package.other_models import Host, User

class File(GModel):
    """ A simple file model.
    
    This model inherits directly from a supplied mixin - in this case, one that
    enables the model to talk to Google's AppEngine database.
    
    If your backend changes, the only code you need to change for this model is
    the inheritance - instead of GModel, put AModel (for example), or whatever 
    is appropriate for your backend.
    """
    ID = IntegerField(primary_key=True) # the primary_key denotes that this 
                                        # field can be used to uniquely 
                                        # identify Files
    name = StringField()
    size = IntegerField()
    type = StringField(max_length=250)  # by default, StringFields are limited 
                                        # to 256 characters. You can limit this
                                        # further by specifying the max_length
                                        # argument.
    notes = StringField()
    created = DateTimeField()
    host = KeyField(Host, type="fk") # Keyfields allow you to specify
                                     # relationships with other models using 
                                     # standard database relations. "fk" here
                                     # indicates that this is a foreign key to
                                     # the Host model
    owner = KeyField(User, type="fk") # There can be multiple KeyFields on each
                                      # each model, just like any other field.
                                      # A KeyField can't be the primary_key,
                                      # though.
    
    def my_size(self):
        """ A function specific to this model, unmanaged by QUI """
        return u"{}".format(to_readable(self.size))