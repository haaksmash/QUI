'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
from fields import Field
from modelmixins import ModelMixin
from fieldmixins import FieldMixin
from model_exceptions import *

class AppEngineModelMix(ModelMixin):
    _port = 80808
    def put(self):
        pass
    
    def _get_interface(self):
        pass
    
    @classmethod
    def get(cls, **kwargs):
        pass
    
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
        #x.put()
        return x

    def __init__(self, *args, **kwargs):
        super(AppEngineModelMix, self).__init__(*args, **kwargs)
        self._db = self.__class__._db if not kwargs.has_key("dbname") else kwargs["dbname"]
        self._host = self.__class__._host if not kwargs.has_key("host") else kwargs["host"]
        self._port = self.__class__._port if not kwargs.has_key("port") else kwargs["port"]

        


class AppEngineFieldMix(FieldMixin):
    def clean(self):
        pass
    
    def translate(self):
        return self.value


