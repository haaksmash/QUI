'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

class Meta(abc.ABCMeta):
    pass


class ModelMixin(object):
    '''Abstract base class for all ModelMixins.
    '''
    __metaclass__ = Meta

    def _get_direct(self, name):
        """ Convenience method to get at Fields directly, if necessary """
        if self._field_names.has_key(name):
            return self._field_names[name]
        elif self._class_fields.has_key(name):
            return self._class_fields[name]
        else:
            return object.__getattribute__(self, name)


    def __getattribute__(self, name):
        """Accessor for a specific attribute of a model by name.
        
        Overriden to make Fields 'invisible'.
        
        Behaves normally for non-Field attributes.
        """
        # ensure that _field_names is a thing
        # (it might not be, on subclasses of user Models)
        try: 
            object.__getattribute__(self, "_field_names")
        except AttributeError:
            self._field_names = {}
            
        if name in object.__getattribute__(self,"_field_names").keys():
            return object.__getattribute__(self, "_field_names")[name].value
        elif name in object.__getattribute__(self, "_class_fields").keys():
            return object.__getattribute__(self, "_class_fields")[name].value
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """Sets a specific attribute of a model
        
        Overriden to make Fields 'invisible'.
        
        Behaves normally for non-Field attributes.
        """
        # check if the attribute exists, then set it if so.
        if name != "_field_names" and name in self._field_names.keys():
            object.__getattribute__(self,"_field_names")[name].value = value
        elif name in object.__getattribute__(self, "_class_fields").keys():
            object.__getattribute__(self, "_class_fields")[name].value = value
        else:
            return object.__setattr__(self, name, value)


    @abc.abstractmethod
    def put(self):
        """Implemented in the specific BackendModelMix classes to put a model instance into the database"""
        pass
    
    @abc.abstractmethod
    def _get_interface(self):
        """Implemented in the specific BackendModelMix to convert from the specific Model instance to whatever 
        backend object we need (for example, json)
        """
        pass
    
    @abc.abstractmethod
    def get(self, pk):
        """ Implemented in the specific BackendModelMix to get a specific model instance from the database.
        Each model instance has a specific, unique primary key. 
        """
        pass
    
    @abc.abstractmethod
    def create(self, **kwargs):
        """ Shortcut method. Creates the model instance and then puts it into the database using .put(). """
        pass

