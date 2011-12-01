from model_exceptions import *
from fields import Field
from utils import get_mixin
from settings import SUPPORTED_BACKENDS

def stored(cls=None, **kwargs):
    """Modifies a class for use with QUI's mixins
    
        Accepts arbitrary keyword arguments, but only acts on
        backend = None
        db = "localhost"
        port = backend-specific-default
        host = "local"
    """
    mixins = {}
    if kwargs.has_key('backend'):
        BEModelMixin = get_mixin(kwargs['backend'])
        mixins['backend'] = BEModelMixin
    else:
        print "no backend in kwargs"
        kwargs['backend'] = None
       

    # we can pass in what we like to the returned function,
    # since it's a decorator!
    def wrapper(cls, mixins=mixins,kwargs=kwargs):
        # ensure backend is defined
        if hasattr(cls, "_backend"):
            mixins['backend'] = get_mixin(getattr(cls, "_backend"))
        elif not kwargs["backend"]:
            raise ImproperlyConfigured("No backend defined: {}".format(cls.__name__))
        elif kwargs["backend"] not in SUPPORTED_BACKENDS:
            raise ImproperlyConfigured("Backend not supported: {}".format(kwargs["backend"]))
        
        
        # add mixins as necessary - potentially more than one
        bases = cls.__bases__
        for key in mixins:
            if mixins[key] not in bases:
                print "Adding {} to {} and its subclasses...".format(mixins[key].__name__, cls.__name__)
                bases = (mixins[key], ) + bases 
        #print cls.__name__
        # the class's typename is the same as before!
        cls = type(cls.__name__, (cls,)+bases, {})
        kwargs["class"] = cls
        
        BEFieldMix = get_mixin(kwargs['backend'], model=False)

        # allow local settings on subclasses to override decorator settings
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
        oldinit = cls.__init__
        def newinit(self, QUIARGS=kwargs, *args, **kwargs):
            if QUIARGS.has_key('_fields_to_init'):
                _fields_to_init = QUIARGS['_fields_to_init']
            else:
                _fields_to_init = {}
            #print dir(self)
            self._field_names = {}
            oldinit(self, *args, **kwargs)
            
            
            for key in dir(self):

                try:
                    if not Field in getattr(self, key).__bases__:
                        continue
                except AttributeError:
                    continue
                #print key
                
                # put appropriate mixin into the field in question
                f = getattr(self, key)
                #print "Found a field - {}:{}".format(key,f) 
                NewF = type(f.__name__, (BEFieldMix,f)+f.__bases__,{})
                #print f.__name__
                #print NewF.__bases__
                
                self._field_names[key] = NewF()
                #delattr(self, key)
            #print _fields_to_init            
            
            


        cls.__init__ = newinit
        
        return cls


    return wrapper

