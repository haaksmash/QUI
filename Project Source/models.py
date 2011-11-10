import abc

from model_exceptions import NoPrimaryKey

class BaseModel(type):
    ### All models will inherit fromt his
    
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


