'''
Created on Dec 3, 2011

@author: haak
'''
from test import FileModel
from fields import BooleanField, IntegerField
from decorators.storage_decorators import stored, subclass
from decorators.field_decorators import class_field


@subclass
class FMSub(FileModel):
    purple = BooleanField
    _host = "google.com"
    
    counter = class_field(IntegerField)
    
    def __init__(self):
        super(FMSub, self).__init__()
        FMSub.counter += 1
        self.purple = False
