'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

from fields import Field
from model_exceptions import *
from decorators import ClassProperty


class ModelMixin(object):
    '''
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def put(self):
        pass
    
    @abc.abstractmethod
    def _get_interface(self):
        pass
    
    @abc.abstractmethod
    def get(cls, pk):
        pass
    
    @abc.abstractmethod
    def create(cls, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        pass

class MDBModelMix(ModelMixin):
    
    _fieldmixin = "MDBFieldMix"    

    
    @classmethod
    def _collection(cls):
        if isinstance(cls, MDBModelMix):
            return cls.__class__._collection()
        return u"{}".format(cls.__name__)
    
    @staticmethod
    def _get_collection(self,conn):
        #self._collection = self.__class__.__name__
        import pymongo
        try:
            db = pymongo.database.Database(conn,self._db)
        except:
            raise ImproperlyConfigured()
        try:
            coll = db[self._collection]
            print "found collection! {}".format(self._collection())
        except Exception:
            import warnings
            warnings.warn("Not a collection: {}; creating new collection".format(self._collection), Warning) 
            coll = pymongo.collection.Collection(db, self._collection(),create=True)
            
        return coll
    
    def put(self):
        import pymongo
        iface = self._get_interface()
        
        conn = pymongo.Connection(host=self._host, port=self._port)
        
        try:
            db = pymongo.database.Database(conn,self._db)
        except:
            raise ImproperlyConfigured()
        try:
            coll = db[self._collection()]
            print "found collection! {}".format(self._collection())
        except Exception:
            import warnings
            warnings.warn("Not a collection: {}; creating new collection".format(self._collection), Warning) 
            coll = pymongo.collection.Collection(db, self._collection(),create=True)
            
        if iface.has_key("_id"):
            print "updating record..."
            coll.save(iface, manipulate=False)
        else:
            print "creating new record..."
            self._id = coll.save(iface, manipulate=True)
            iface.update({"_id":self._id})
            
        #conn.end_request()
        return iface
    
    def _get_interface(self):
        json = {}
        for key in dir(self):
            # skip private and special members
            if key[0] == "_" and (key != "_{}__id".format(self.__class__.__name__) and key != "_id"):
                continue
            if hasattr(getattr(self, key), "__call__"):
                # some fields may be callable - catch their values.
                if hasattr(getattr(self, key),"value"):
                    value = getattr(self,key).value
                else:
                    continue
            else:
                value = getattr(self,key)
                
            
            
            json.update({key:value})
        
        return json
    
    @classmethod
    def get(cls, **kwargs):
        from bson.objectid import ObjectId
        import pymongo
        conn = pymongo.Connection(host=cls._host, port=cls._port)
        
        coll = MDBModelMix._get_collection(cls, conn)
        
        
        if kwargs.has_key("pk"):
            if not isinstance(kwargs["pk"], ObjectId):
                try:
                    spec = ObjectId(kwargs["pk"])
                except:
                    raise InvalidUserPK
                
        else:
            spec = kwargs
        x = coll.find(spec=spec)
        obj = [cls.create(**y) for y in x]
        return obj
    
    @classmethod
    def create(cls, **kwargs):
        # if they have special constructor arguments...
        if kwargs.has_key("init_args"):
            x = cls(kwargs["init_args"])
        else:
            x = cls()
        
        #attach instance thingies
        for key in kwargs.keys():
            try:
                setattr(x, key, kwargs[key])
            except AttributeError:
                print "can't set {}".format(key)
        
        #autostore created instances
        x.put()
        return x

    def __init__(self, *args, **kwargs):
        super(MDBModelMix, self).__init__(*args, **kwargs)
        self._db = self.__class__._db if not kwargs.has_key("dbname") else kwargs["dbname"]
        self._host = self.__class__._host if not kwargs.has_key("host") else kwargs["host"]
        self._port = self.__class__._port if not kwargs.has_key("port") else kwargs["port"]
        if kwargs.has_key("collection"):
            self._collection = kwargs["collection"]
        
        
    
