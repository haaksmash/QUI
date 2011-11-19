'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

from fields import Field
from model_exceptions import ImproperlyConfigured

class ModelMixin(object):
    '''
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def put(self):
        pass
    
    @abc.abstractmethod
    def get_interface(self):
        pass
    
    @classmethod
    @abc.abstractmethod
    def get(cls, pk):
        pass
    
    @classmethod
    @abc.abstractmethod
    def create(cls, **kwargs):
        pass


    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        pass

class MDBModelMix(ModelMixin):

    def put(self):
        import bson
        import pymongo
    
        iface = self.get_interface()
        
        conn = pymongo.Connection(host=self._host, port=self._port)
        
        try:
            db = pymongo.database.Database(conn,self._db)
        except:
            raise ImproperlyConfigured()
        try:
            coll = db[self._collection]
            print "found collection! {}".format(self._collection)
        except Exception:
            import warnings
            warnings.warn("Not a collection: {}; creating new collection".format(self._collection), Warning) 
            coll = pymongo.collection.Collection(db, self._collection,create=True)
            
        coll.save(iface, manipulate=False)
        return iface
    
    def __len__(self):
        count = 0
        for el in self.__dict__:
            if isinstance(self.__dict__[el], Field):
                count += 1
            continue
        
        return count
    
    def __iter__(self):     
        for el in self.__dict__:
            if isinstance(self.__dict__[el], Field):
                yield el
            continue
    
    def __getitem__(self, key):
        if key in self.__dict__:
            key = self.__dict__[key]
            if isinstance(key, Field):
                return key.value
        return None
    
    def iteritems(self):
        for key in self:
            yield (key, self[key])
            
    
    def get_interface(self):
        json = {}
        for key,value in self.iteritems():
            json.update({key:value})
        
        return json
    
    def get(cls, pk):
        pass
    
    def create(cls, **kwargs):
        pass
        #result = None
        
        #result.put()
        #return result
    
    def __init__(self, *args, **kwargs):
        super(MDBModelMix, self).__init__(*args, **kwargs)
        self._db = "local"
        self._host = "localhost"
        self._port = 27017
        self._collection = u"{}".format(self.__class__.__name__)
        
        
    