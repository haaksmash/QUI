class NoPrimaryKey(Exception):
    """No primary key is defined for this model"""
    pass

class TooManyPKs(Exception):
    """Tried to define multiple PKs for this model"""
    pass

class InvalidUserPK(NoPrimaryKey):
    """user-defined pk does not exist"""

class ObjectDoesNotExist(Exception):
    "The requested object does not exist"
    silent_variable_failure = True
    
class MultipleObjectsReturned(Exception):
    "The query returned multiple objects when only one was expected."
    pass

class ImproperlyConfigured(Exception):
    pass