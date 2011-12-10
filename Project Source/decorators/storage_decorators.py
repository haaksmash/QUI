from quiexceptions.model_exceptions import *
from fields import Field, ClassField
from utils import get_mixin
from settings import SUPPORTED_BACKENDS


def stored(cls=None, **kwargs):
    """Modifies a class for use with QUI's mixins
    
    Accepts arbitrary keyword arguments, but only acts on
    backend = None
    db = "localhost"
    port = backend-specific-default
    host = "local"
    
    this decorator does all the work that QUI needs to do; adds mixins to the class and
    any fields that the class happens to have defined.
        
    """
    required_kwargs = []
    mixins = {}
    
    if kwargs.has_key('backend'):
        if not isinstance(kwargs['backend'], basestring):
            raise TypeError("backend keyword argument expects a string")
        BEModelMixin = get_mixin(kwargs['backend'])
        
        mixins['modelmix'] = BEModelMixin
        """
        # The following is the result of an experiment to allow users to define
        # model- and fieldmixins manually, if they so wished (if they had custom
        # defined their own fieldmixin, for example, but were satisfied with
        # the supplied modelmixin.
        # Results were promising, but presented issues that we didn't have time to deal
        # with before submission time.
        
    elif kwargs.has_key('modelmix'):
        if isinstance(kwargs['modelmix'], basestring):
            raise TypeError("modelmix keyworkd argument can't be a string")
        
        BEModelMixin = kwargs['modelmix']
        
        required_kwargs += [("fieldmix", "required for a manually defined model mixin")]
        
        mixins['modelmix'] = BEModelMixin
        kwargs['backend'] = True
        """
    else:
        kwargs['backend'] = None
        required_kwargs += [("backend", "unless 'modelmix' and 'fieldmix' are defined instead.")]
       
    # make sure that we have all the required settings to proceed
    missing_kwargs = []
    for arg in required_kwargs:
        if not kwargs.has_key(arg[0]):
            missing_kwargs += [arg]
    if len(missing_kwargs) != 0:
        raise ImproperlyConfigured("You need to supply the following keyword arguments to the storage decorator:\n {}".format(", ".join(missing_kwargs)))
    
    
    # we can pass in what we like to the returned function,
    # since it's a decorator!
    def wrapper(cls, mixins=mixins,kwargs=kwargs):
        # ensure backend is defined
        if hasattr(cls, "_backend"):
            if isinstance(cls._backend, basestring):
                mixins['modelmix'] = get_mixin(getattr(cls, "_backend"))
            
            #elif isinstance(cls._backend, bool):
            #    mixins['modelmix'] = cls._modelmix
                
            else:
                raise TypeError("_backend attribute must be a string")
            
            """
            # further relics of the manual specification experiment; left in
            # because we'd like to work on this more later.
            
        elif not kwargs["backend"]:
            try:
                mixins['modelmix'] 
            except Exception, e: 
                raise ImproperlyConfigured("No backend defined: {}\n{}".format(cls.__name__,e))
            """
            
        else:
            setattr(cls, "_backend", kwargs['backend'])
            #setattr(cls, "_modelmix", mixins['modelmix'])
        
        
        # add mixins as necessary - potentially more than one
        bases = cls.__bases__
        for key in mixins:
            if mixins[key] not in cls.__mro__:
                #print "Adding {} to {} and its subclasses...".format(mixins[key].__name__, cls.__name__)
                bases = (mixins[key], ) + bases 
        
        # ensures the class's typename is the same as before!
        cls = type(cls.__name__, (cls,)+bases, {})
        kwargs["class"] = cls
        
        # allows manual fieldmix specification
        if hasattr(cls, "_fieldmix"):
            BEFieldMix = cls._fieldmix
        
        elif kwargs.has_key("fieldmix"):
            if isinstance(kwargs['fieldmix'],basestring):
                raise TypeError("fieldmix keyword must be a class, not a string")
            
            BEFieldMix = kwargs['fieldmix']
            setattr(cls, "_fieldmix", BEFieldMix)
        elif hasattr(cls, "_backend"):
            BEFieldMix = get_mixin(cls._backend, model=False)
        else:
            BEFieldMix = get_mixin(kwargs["backend"], model=False)
        #setattr(cls, "_fieldmix", BEFieldMix)
        
        # nab any ClassFields and initialize them at decoration time,
        # so they're available immediately (as we'd expect)
        setattr(cls, "_class_fields", {})
        for key in dir(cls):
            try:
                if not Field in getattr(cls, key).__mro__:
                    continue
            except AttributeError:
                continue
            
            f = getattr(cls, key)
            if ClassField in f.__bases__:
                #print key, f, f.__bases__
                NewF = type(f.__name__, (BEFieldMix,f)+f.__bases__,{})
                #print NewF.__bases__
                if hasattr(cls, "Options") and hasattr(cls.Options,key):
                    options = getattr(cls.Options,key)
                else:
                    options = {}
                setattr(cls, key, NewF(**options))

                cls._class_fields[key] = getattr(cls, key)
                
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
         
        ##############
        # alter the class's __init__, as necessary, for init'ing of fields and such.
        
        #
        oldinit = cls.__init__
        def quiinit(self, QUIARGS=kwargs, *args, **kwargs):
            #print "Entering Modified init..."
            # make sure that QUIARGS is actually a dict-like object
            # if we're modifying the init of a subclass of a Model, it's the subclass.
            if isinstance(QUIARGS, dict):
                if QUIARGS.has_key('_fields_to_init'):
                    _fields_to_init = QUIARGS['_fields_to_init']
                else:   
                    _fields_to_init = {}
                if QUIARGS.has_key('_field_names'):
                    self._field_names = QUIARGS['_field_names']
            else:
            #print dir(self)
                self._field_names = {}
            
            
            
            for key in dir(self):

                try:
                    if not Field in getattr(self, key).__bases__:
                        continue
                except AttributeError:
                    continue
                #print key
                
                
                f = getattr(self, key)
                #print "Found a field - {}:{}".format(key,f) 
                
                # put appropriate mixin into the field in question
                NewF = type(f.__name__, (BEFieldMix,f)+f.__bases__,{})
                
                # if it has any options set for it, use them in the init
                if hasattr(cls, "Options") and hasattr(cls.Options,key):
                    options = getattr(cls.Options,key)
                else:
                    options = {}
                self._field_names[key] = NewF(**options)
                
            #print "returning to user-defined init..."
            oldinit(self, *args, **kwargs)
                        
            
            


        cls.__init__ = quiinit
        
        return cls


    return wrapper


def subclass(cls):
    """Initializes any subclass-wide fields, without doing all the work that @stored does.
       
    This decorator requires that a class have the _backend attribute defined. 
    """
    
    if "_class_fields" in dir(cls):
        pass
    else:
        pass
    
    BEFieldMix = get_mixin(cls._backend, model=False)
    
    for key in dir(cls):
        try:
            if Field not in getattr(cls, key).__mro__:
                continue
        except AttributeError:
            continue
        f = getattr(cls, key)
        
        if ClassField not in f.__mro__:
            continue
        
        NewF = type(f.__name__, (BEFieldMix, f)+f.__bases__, {})
        if hasattr(cls, "Options") and hasattr(cls.Options,key):
                options = getattr(cls.Options,key)
        else:
            options = {}
        setattr(cls, key, NewF(**options))
        cls._class_fields[key] = getattr(cls, key)
        
    return cls
