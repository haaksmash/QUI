'''
Created on Dec 1, 2011

@author: haak
'''


def primary_key(cls):
    """Marks a field as a primary key.
    """
    oldinit = cls.__init__
    def newinit(self, *args, **kwargs):
        oldinit()
        self._primary_key = True
        
    cls.__init__ = newinit
    return cls