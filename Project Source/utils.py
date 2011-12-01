'''
Created on Dec 1, 2011

@author: haak
'''
from model_exceptions import ImproperlyConfigured
from settings import SUPPORTED_BACKENDS
# helper method for loading backend classes
def get_mixin(name, model=True):
    try:
        #print "getting: {}ModelMix".format(name)
        module = __import__("{}Mixins".format(name))
        if model:
            backend = getattr(module, "{}ModelMix".format(name))
        else:
            backend = getattr(module, "{}FieldMix".format(name))
    except:
        raise ImproperlyConfigured("Backend not supported: {}\nsupported backends: {}".format(name, SUPPORTED_BACKENDS))
    
    return backend
