from model_exceptions import *



SUPPORTED_BACKENDS = ["appengine","simpledb", "mongodb",]

class OProperty(object):
    """Based on the emulation of PyProperty_Type() in Objects/descrobject.c"""
    
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError, "unreadable attribute"
        if self.fget.__name__ == '<lambda>' or not self.fget.__name__:
            return self.fget(obj)
        else:
            return getattr(obj, self.fget.__name__)()
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError, "can't set attribute"
        if self.fset.__name__ == '<lambda>' or not self.fset.__name__:
            self.fset(obj, value)
        else:
            getattr(obj, self.fset.__name__)(value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError, "can't delete attribute"
        if self.fdel.__name__ == '<lambda>' or not self.fdel.__name__:
            self.fdel(obj)
        else:
            getattr(obj, self.fdel.__name__)()

def get_backend(name):
    from modelmixins import MDBModelMix
    if name == "mongodb":
        return MDBModelMix

def stored(cls=None, **kwargs):
    from modelmixins import MDBModelMix
    from fieldmixins import MDBFieldMix
    from fields import Field
    """if cls:
        bases = (cls,)+cls.__bases__
        mixins = []
        cls = type(cls.__name__, bases, {})
        return cls     
    else:"""
    mixins = []
    if kwargs.has_key('backend'):
        if kwargs['backend'] == 'mongodb':
            mixins = [MDBModelMix]+mixins
    else:
        kwargs['backend'] = None
       

    # we can pass in what we like to the returned function,
    # since it's a decorator!
    def wrapper(cls, mixins=mixins,kwargs=kwargs):
        if hasattr(cls, "_backend"):
            mixins = [get_backend(getattr(cls, "_backend"))]
        elif not kwargs['backend']:
            raise ImproperlyConfigured("No backend defined: {}".format(cls.__name__))
            mixins = []
        bases = (cls,)+cls.__bases__
        
        for mix in mixins:
            if mix not in bases:
                print "Adding {} to {}...".format(mix, cls.__name__)
                bases = (mix, ) + bases 
        cls = type(cls.__name__, bases, {})
        
        if not hasattr(cls, "_fieldmixin"):
            raise ImproperlyConfigured("No fieldmixin defined: {}".format(cls.__name__))
       
        # Having identified the fieldmixin for this class,
        # put said mixin into all of the Field subclasses
        # we can find, but don't initialize them just yet.
        fields_to_init = {}
        for key in dir(cls):
            try:
                if not Field in getattr(cls, key).__bases__:
                    continue
            except AttributeError:
                continue
            
            f = getattr(cls, key)
            class NewF(MDBFieldMix, f):
                pass
            
            fields_to_init[key] = NewF
        if fields_to_init != {}:
            kwargs['_fields_to_init'] = fields_to_init

        # where is the model stored?
        if kwargs.has_key("db"):
            setattr(cls, "_db", kwargs["db"])
        elif not hasattr(cls, "_db"):
            setattr(cls, "_db", "local")
            
        if kwargs.has_key("host"):
            setattr(cls, "_host", kwargs["host"])
        elif not hasattr(cls, "_host"):
            setattr(cls, "_host", "localhost")
            
        if kwargs.has_key("port"):
            setattr(cls, "_db", int(kwargs["port"]))
        elif not hasattr(cls, "_port"):
            raise ImproperlyConfigured("no port for model:{}".format(cls.__name__)) 
        
        # alter the class's __init__, as necessary,
        # to initialize any Fields that we encountered above.
        oldinit = cls.__init__
        def newinit(self, *args, **kwargs):
            if kwargs.has_key('_fields_to_init'):
                _fields_to_init = kwargs.pop('_fields_to_init')
            else:
                _fields_to_init = None
            
            oldinit(self, *args, **kwargs)
            
            # initialize fields!
            if _fields_to_init != None:
                for key, value in _fields_to_init:
                    setattr(self, key, value())


        cls.__init__ = newinit
        
        return cls
    return wrapper


def primary_key(cls):
    """Marks a field as a primary key.
    """
    oldinit = cls.__init__
    def newinit(self, *args, **kwargs):
        oldinit()
        self._primary_key = True
        
    cls.__init__ = newinit
    return cls
