'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc
import os, sys
current_dir = os.getcwd()
#from backends.google.google.appengine.ext import db
from bson.son import SON





from fields import *

class FieldMixin(object):
    """
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def clean(self):
        raise NotImplementedError("This backend has no way to sanitize data")
    
    @abc.abstractmethod
    def translate(self):
        raise NotImplementedError("This backend has no way to format data")
    
    def __init__(self, *args, **kwargs):
        # need to make sure the Field ancestor's init is called
        super(FieldMixin, self).__init__(*args, **kwargs)
    
"""
class GFieldMix(FieldMixin):
    
    def clean(self):
        print "make sure data is sanitary here!"
        self.cleaned_data = self.value
        
    def translate(self):
        if isinstance(self, StringField):
            print "Translate a StringField"
            translation = db.StringProperty()
            
            return translation
"""
class MDBFieldMix(FieldMixin):
    def clean(self):
        pass
    
    def translate(self):
        return self.value

    
class Test(MDBFieldMix, StringField):
    pass