class NoPrimaryKey(Exception):
    """No primary key is defined for this model"""
    pass

class TooManyPKs(Exception):
    """Tried to define multiple PKs for this model"""
    pass

class InvalidUserPK(NoPrimaryKey):
    """user-defined pk does not exist"""
