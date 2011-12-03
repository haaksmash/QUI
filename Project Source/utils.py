'''
Created on Dec 1, 2011

@author: haak
'''
from model_exceptions import ImproperlyConfigured
from settings import SUPPORTED_BACKENDS
# helper method for loading backend classes
def get_mixin(name, model=True):
    try:
        #print "getting: {}Mixins".format(name)
        if model:
            getter = "{}ModelMix"
        else:
            getter = "{}FieldMix"
            
        module = __import__("{}Mixins".format(name),fromlist=[getter.format(name.split(".")[-1])])
        #print "got module"
        # if they gave a complicated path to the mixin
        name = name.split(".")[-1]
        if model:
            backend = getattr(module, "{}ModelMix".format(name))
        else:
            backend = getattr(module, "{}FieldMix".format(name))
    except Exception, e:
        raise ImproperlyConfigured("Backend not supported: {}\n inherently supported backends: {}\
                                    \n got error: {}".format(name, ", ".join(SUPPORTED_BACKENDS), e))
   
    return backend
