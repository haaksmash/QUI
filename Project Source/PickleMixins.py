'''
@author: Haak Saxberg and Jess Hester

This mixin simply employs Python's pickling abilities. Model instances
are stored in a directory for that model (inside of the QUI directory), 
and can be gotten from the same place.
'''
import os
from fields import Field
from modelmixins import ModelMixin
from fieldmixins import FieldMixin
from quiexceptions.model_exceptions import *
import pickle,abc

class PickleModelMix(ModelMixin):
    # Default port, won't really matter
    _port = 0
    def put(self):
        """ Take the model instance and store it in a file
            under ModelName/self.id (to make sure the file name
            is unique)
        """
        dir = self.__class__.__name__
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = os.path.join(dir, self.name)
        f = open(filename,"w")
        pickle.dump(self, f)
        f.close()
    
    @classmethod        
    def get(cls, **kwargs):
        if kwargs.has_key("pk"):
            dir = cls.__name__
            if not os.path.exists(dir):
                raise ObjectDoesNotExist
            filename = os.path.join(dir,kwargs['pk'])
            f = open(filename,"r")
            return pickle.load(f)
        else:
            raise ObjectDoesNotExist
        
    @classmethod
    def create(cls, **kwargs):
        # if they have special constructor arguments...
        if kwargs.has_key("init_args"):
            x = cls(**kwargs["init_args"])
        else:
            x = cls()
        
        #attach instance thingies
        for key in kwargs.keys():
            try:
                setattr(x, key, kwargs[key])
            except AttributeError:
                print "can't set {}".format(key)
        
        #autostore created instances
        x.put()
        return x
    
    def _get_interface(self):
        pass
    
class PickleFieldMix(FieldMixin): 
    def clean(self):
        pass
    
    def translate(self):
        return self.value