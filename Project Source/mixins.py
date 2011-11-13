'''
Created on Nov 10, 2011

@author: haak
'''
import abc

class Storable(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta
    
    _meta = {}
    
    
    @classmethod
    def _get(cls):
        print "getting from {}".format(cls._meta['backend'])
        
    def put(self):
        print "storing to {}".format(self.__class__._meta['backend'])
        
    def __init__(self):
        self._meta['backend'] = None
        pass

class Stored_in_Appengine(Storable):
    
    @classmethod
    def _get(cls):
        super(Stored_in_Appengine)._get()
        print "\t-from appengine mixin"
        
    def put(self):
        super(Stored_in_Appengine, self)._store()
        print "\t-from appenging mixin"
        
    def __init__(self):
        super(Stored_in_Appengine, self).__init__()
        self._meta['backend'] = "appengine"
        
class Stored_in_SimpleDB(Storable):
    
    @classmethod
    def _get(cls):
        super(Stored_in_SimpleDB)._get()
        print "\t-from simpledb mixin"
        
    def put(self):
        super(Stored_in_SimpleDB, self)._store()
        print "\t-from simpledb mixin"
        
    
    def __init__(self):
        super(Stored_in_SimpleDB, self).__init__()
        self._meta['backend'] = "simpledb"