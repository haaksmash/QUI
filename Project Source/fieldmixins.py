'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester

This is the abstract base class for field mixins for different backends.
'''
import abc
import os, sys
from fields import *

class FieldMixin(object):
    """Abstract base class for field mixin objects for specific backends. These methods 
    generally only need to pass, and are optional features.
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def clean(self):
        """ Can be implemented in the specific backend FieldMixin. Ensures data is 
        sanitized and can safely be inserted into the database.
        """
        raise NotImplementedError("This backend has no way to sanitize data")
    
    @abc.abstractmethod
    def translate(self):
        """ Ideally, is implemented in the specific backend FieldMixin to convert from a
        model field object to the backend database field object 
        """
        raise NotImplementedError("This backend has no way to format data")
    
    def __init__(self, *args, **kwargs):
        # need to make sure the Field ancestor's init is called
        super(FieldMixin, self).__init__(*args, **kwargs)
    
