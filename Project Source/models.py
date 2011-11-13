'''
Created on Nov 10, 2011

@author: haak
'''
import abc

from model_exceptions import *

class BaseModel(type):
    ### All models will inherit fromt his
    
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            # not a model, nothing special:
            return super_new(cls, name, bases, attrs)
        
        #create class
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, module)
    
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        base_meta = getattr(new_class, "_meta", None)
    
        new_class.add_to_class('_meta', meta)
        if not abstract:
            new_class.add_to_class('DNE', subclass_exception('DNE',
                                                             tuple(x.DoesNotExist
                                                                        for x in parents if hasattr(x, '_meta') and not x._meta.abstract)
                                                             or (ObjectDoesNotExist,), module))
            new_class.add_to_class('MultipleReturns', subclass_exception('MultipleObjectsReturned',
                                                             tuple(x.MultipleObjectsReturned
                                                                        for x in parents if hasattr(x, '_meta') and not x._meta.abstract)
                                                             or (MultipleObjectsReturned,), module))
            if base_meta and not base_meta.abstract:
                if not hasattr(meta, 'ordering'):
                    new_class._meta.ordering = base_meta.ordering
                if not hasattr(meta, 'get_latest_by'):
                    new_class._meta.get_latest_by = base_meta.get_latest_by
                    
        if getattr(new_class, '_default_manager', None):
            new_class._default_manager = new_class.default_manager._copy_to_model(new_class)
            new_class._base_manager = new_class._base_manager._copy_to_model(new_class)
            
        m = get_model(new_class._meta.app_label, name)
        if m is not None:
            return m
        
    
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

class ModelState(object):
    def __init__(self, db=None):
        self.db = db
        self. adding = True

class Model(object):
    __metaclass__ = BaseModel

    def __init__(self, *args, **kwargs):
        if not hasattr(kwargs, "primary_key"):
            raise NoPrimaryKey
        
        self._state = ModelState()

        if kwargs:
            for key in kwargs:
                if isinstance(getattr(self.__class__, prop), property):
                    setattr(self, prop, kwargs.pop(prop))

        if kwargs:
            raise TypeError("'{}' is an invalid kwarg for this function".format(kwargs.keys()[0]))

        super(Model, self).__init__()

def subclass_exception(name, parents, module):
    return type(name, parents, {'__module__': module})
