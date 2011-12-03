from quiexceptions import QUIModelException, DNEException


class PKError(QUIModelException):
    pass

class NoPrimaryKey(PKError):
    """No primary key is defined for this model"""
    pass

class TooManyPKs(PKError):
    """Tried to define multiple PKs for this model"""
    pass

class InvalidUserPK(PKError):
    """user-defined pk does not exist"""

class ObjectDoesNotExist(QUIModelException, DNEException):
    "The requested object does not exist"
    silent_variable_failure = True
    
class MultipleObjectsReturned(QUIModelException):
    "The query returned multiple objects when only one was expected."
    pass

class ImproperlyConfigured(QUIModelException):
    pass