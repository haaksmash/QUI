from quiexceptions import QUIException

class NoPrimaryKey(QUIException):
    """No primary key is defined for this model"""
    pass

class TooManyPKs(QUIException):
    """Tried to define multiple PKs for this model"""
    pass

class InvalidUserPK(NoPrimaryKey):
    """user-defined pk does not exist"""

class ObjectDoesNotExist(QUIException):
    "The requested object does not exist"
    silent_variable_failure = True
    
class MultipleObjectsReturned(QUIException):
    "The query returned multiple objects when only one was expected."
    pass

class ImproperlyConfigured(QUIException):
    pass