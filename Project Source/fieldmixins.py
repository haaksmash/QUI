'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc
from fields import *
from backends.google.google.appengine.ext import db


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
    
    def __init__(self, **kwargs):
        pass
    
    
class GFieldMix(FieldMixin):
    
    def clean(self):
        print "make sure data is sanitary here!"
        self.cleaned_data = self.value
        
    def translate(self):
        if isinstance(self, StringField):
            print "Translate a StringField"
            translation = db.StringProperty()
            
            return translation