from model_exceptions import *

from mixins import *

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

def stored_hello(self, name="bob"):
    print "Hello, {}! Love, {}".format(name, self)

def stored_store(self, *args, **kwargs):
    print "Storing a {} to {}".format(self.__class__, self._meta['backend'])
    print "Attrs:"
    for key, prop in self.__dict__.iteritems():
        print "\t{} : {}".format(key, prop)
    print "{}".format([x for x in self.__class__.__dict__.iteritems() if "__" not in x[0]])

class Primary_Key(object):
    def __init__(self, attribute):
        setattr(attribute, "primary_key", True)
        self.attribute = attribute

    def __call__(self, *args, **kwargs):
        return self.attribute.__call__(self, *args, **kwargs)
    
    def __get__(self, *args, **kwargs):
        return self.attribute.__get__(*args, **kwargs)



#class stored:
class Stored_Direct(object):
    # Makes our decorator actually work with a class
    def __call__(self, *args, **kwargs):
        
        oldinit = self.cls.__init__
        
        def mod_init(func, *args, **kwargs):
            """
                Allows us to hook into the class's init, and perform pre-processing
                if necessary.
            """
            print "decorator replaced me"
            
            return func
            
        self.cls.__init__ = mod_init(oldinit)
        return self.cls.__call__(*args, **kwargs)
        

    def __get__(self, *args, **kwargs):
        return self.cls.__get__(*args, **kwargs)

    # Class-wide methods should be defined in the decorator
    def get(self, *args, **kwargs):
        print "getting a {} from {}".format(self.cls, self.cls._meta['backend'])

    def __init__(self, cls, *args, **kwargs):
        """
            initialization for decorator - called once for each decorated class
        """
        oldnew = cls.__new__
        def modnew(func, cls, *args, **kwargs):
            for name in [x for x in globals() if "stored_" in x]:
                setattr(cls, name[7:], globals()[name])
            print "Defining storage class for {}".format(cls.__name__)
            _meta = {}
            _meta["backend"] = kwargs['backend'] if kwargs.has_key("backend") else None
            if _meta['backend'] not in SUPPORTED_BACKENDS:
                raise Exception(r"Not a supported database: {}".format(_meta['backend']))
    
            pk = kwargs['primary_key'] if kwargs.has_key("primary_key") else None
            if pk:
                try:
                    getattr(cls, pk)
                except AttributeError:
                    raise InvalidUserPK(r"{} is not a field in {}".format(pk, cls))
    
            if not pk:
                raise NoPrimaryKey("No primary key defined for {}".format(cls))
            
    
            # store in instance, so we can get to it later
            setattr(cls, "_meta", _meta)
            return func
        cls.__new__ = modnew(oldnew, cls, *args, **kwargs)
        
        self.cls = cls

#    def __init__(self, db=None, primary_key=None):
#        pass


class Stored_Mixin(object):
    def __call__(self, *args, **kwargs):
        return self.cls.__call__(*args, **kwargs)
    
    def __get__(self, *args, **kwargs):
        return self.cls.__get__(*args, **kwargs)
    
    def __init__(self, cls, *args, **kwargs):
        cls.__bases__ +=  (Storable,)



def stored_direct(cls=None, db="appengine", primary_key=None):
    """
        This decorater allows users to decorate with or
        without a specified backend as their storage
        engine
    """
    if cls:
        return Stored_Direct(cls)
    else:
        def wrapper(cls):
            return Stored_Direct(cls, backend=db, primary_key=primary_key)

    return wrapper


def stored_mixin(cls=None, *args, **kwargs):
    if cls:
        bases = (cls,)+cls.__bases__
        mixins = []
        cls = type(cls.__name__, (Stored_in_Appengine,) + bases, {})
        return cls     
    else:
        mixins = []
        if kwargs.has_key('db'):
            if kwargs['db'] == 'simpledb':
                mixins = [Stored_in_SimpleDB]+mixins
        else:
            mixins = [Stored_in_Appengine] + mixins
            
        def wrapper(cls):
            bases = (cls,)+cls.__bases__
            
            for mix in mixins:
                if mix not in bases:
                    print "Adding {} to {}...".format(mix, cls.__name__)
                    bases = (mix, ) + bases 
            cls = type(cls.__name__, bases, {})
            return cls
    return wrapper
