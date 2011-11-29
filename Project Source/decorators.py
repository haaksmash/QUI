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
        
    def wrapper(cls):
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
        
        #print "Creating a {} with fieldmixin {}".format(cls.__name__, cls._fieldmixin)
        for key in dir(cls):
            #print key               
            try:
                if not Field in getattr(cls, key).__bases__:
                    continue
            except AttributeError:
                continue
            
            f = getattr(cls, key)
            class NewF(MDBFieldMix, f):
                pass
            
            setattr(cls, key, NewF())
        
        # where is the model stored?
        if kwargs.has_key("db"):
            setattr(cls, "_db", kwargs["db"])
        elif not hasattr(cls, "_db"):
            setattr(cls, "_db", "local")
            
        if kwargs.has_key("host"):
            setattr(cls, "_host", kwargs["host"])
        elif not hasattr(cls, "_host"):
            setattr(cls, "_host", "labrain.st.hmc.edu")
            
        if kwargs.has_key("port"):
            setattr(cls, "_db", int(kwargs["port"]))
        elif not hasattr(cls, "_port"):
            setattr(cls, "_port", 27019)
        
        oldinit = cls.__init__
        def newinit(self, *args, **kwargs):
            oldinit(self, *args, **kwargs)
            #self._collection = self.__class__.__name__
        cls.__init__ = newinit
        """
        clsnew = cls.__new__
        def newnew(cls, *args, **kwargs):
            cls = clsnew(cls, *args, **kwargs)
            setattr(cls, "_collection", cls.__name__)
            return cls
        cls.__new__ = newnew
        """
        return cls
    return wrapper


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

def primary_key(cls):
    oldinit = cls.__init__
    def newinit(self, *args, **kwargs):
        oldinit()
        self._primary_key = True
        
    cls.__init__ = newinit
    return cls