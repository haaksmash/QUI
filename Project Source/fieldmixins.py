'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc
import os, sys
#from backends.google.google.appengine.ext import db

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
    
