'''
Created on Dec 1, 2011

@author: haak
'''

from fields import Field, ClassField, FieldDNE



def primary_key(cls):
    """Marks a field as a primary key. 
    This function does not currently influence QUI's behavior in any way.
    
    TODO: make a PrimaryKey field class, same as ClassField 
    """
    oldinit = cls.__init__
    def newinit(self, *args, **kwargs):
        oldinit()
        self._primary_key = True
        
    cls.__init__ = newinit
    return cls


def class_field(cls):
    """Marks a field as a class-wide field.
        Raises an error if given a non-Field class.
    """
    if not Field in cls.__mro__:
        raise FieldDNE("Not a field: {}".format(cls.__name__))

    class NewF(cls, ClassField, Field):
        pass
    #print cls.__bases__
    NewF.__name__ = cls.__name__
    return NewF