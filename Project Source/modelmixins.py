'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

from model_exceptions import *


class ModelMixin(object):
    '''Abstract base class for all ModelMixins.
    
    
    
    '''
    __metaclass__ = abc.ABCMeta

    def _get_direct(self, name):
        """ Convenience method to get at Fields directly, if necessary """
        if self._field_names.has_key(name):
            return self._field_names[name]
        else:
            return object.__getattribute__(self, name)


    def __getattribute__(self, name):
        """Overriden to make Fields 'invisible'.
        
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
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """Overriden to make Fields 'invisible'.
        
        Behaves normally for non-Field attributes.
        """
        if name != "_field_names" and name in self._field_names.keys():
            object.__getattribute__(self,"_field_names")[name].value = value
        else:
            return object.__setattr__(self, name, value)


    @abc.abstractmethod
    def put(self):
        pass
    
    @abc.abstractmethod
    def _get_interface(self):
        pass
    
    @abc.abstractmethod
    def get(self, pk):
        pass
    
    @abc.abstractmethod
    def create(self, **kwargs):
        pass

