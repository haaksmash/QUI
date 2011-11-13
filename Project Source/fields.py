'''
Created on Nov 10, 2011

@author: Haak Saxberg and Jess Hester
'''

class FieldDNE(Exception):
    pass

class Field(object):
    creation_counter = 0
    
    default_error_messages = {
                              'null':_(u"This field cannot be null"),
                              'blank':_(u"This field cannot be blank"),
                              'unique':_(u"{model} with this {field} already exists"),
                              }
    
    def _description(self):
        return u"Field <{type}>".format(**{"type":self.__class__.__name__})
    
    description = property(_description)
    
    def __init__(self, **kwargs):
        pass
    
    def __cmp__(self, rhs):
        pass
    
    def __deepcopy__(self, memodict):
        pass
    
    def to_python(self, value):
        pass
    
    def db_type(self, connection):
        pass
    
    @property
    def unique(self):
        return self._unique or self.primary_key
    
    