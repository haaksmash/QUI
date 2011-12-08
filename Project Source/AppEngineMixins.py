'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import os
from fields import Field
from modelmixins import ModelMixin
from fieldmixins import FieldMixin
from quiexceptions.model_exceptions import *
from google.appengine.ext import db
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import datastore
from google.appengine.api import capabilities
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.datastore import datastore_pb
from google.appengine.datastore import datastore_query
from google.appengine.datastore import datastore_rpc
from google.appengine.datastore import entity_pb

class AppEngineModelMix(ModelMixin):
    _port = 8080
    _app_id = 'helloworld'
    os.environ['APPLICATION_ID'] = _app_id
#    datastore_file = os.path.join(os.path.dirname(__file__),'data')
#    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
#    stub = datastore_file_stub.DatastoreFileStub(_app_id, datastore_file, '/')
#    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
        
    def put(self, **kwargs):
        print "Putting to AppEngine at {}:{}".format(self._host, self._port)
       # datastore.Put(datastore.Entity(self._get_interface()),**kwargs)
        datastore.Put(datastore.Entity("String",_app=self._app_id,unindexed_properties=self._get_interface()))
        
    def _get_interface(self):
        x = {}
        for el in dir(self):
            if "_" == el[0]:
                continue
            if hasattr(getattr(self, el), "__call__"):
                continue
            
            x[el] = getattr(self, el)
        return x
    
    @classmethod
    def get(cls, **kwargs):
        print "Getting from AppEngine"
    
    @classmethod
    def create(cls, **kwargs):
        # if they have special constructor arguments...
        if kwargs.has_key("init_args"):
            x = cls(**kwargs["init_args"])
        else:
            x = cls()
        
        #attach instance thingies
        for key in kwargs.keys():
            try:
                setattr(x, key, kwargs[key])
                print key
            except AttributeError:
                print "can't set {}".format(key)
        
        #autostore created instances
        x.put()
        return x

#    def __init__(self, *args, **kwargs):
#        super(AppEngineModelMix, self).__init__(*args, **kwargs)
#        print 'in init'
#        self._db = self.__class__._db if not kwargs.has_key("dbname") else kwargs["dbname"]
#        self._host = self.__class__._host if not kwargs.has_key("host") else kwargs["host"]
#        self._port = self.__class__._port if not kwargs.has_key("port") else kwargs["port"]

#        


class AppEngineFieldMix(FieldMixin):
    def clean(self):
        pass
    
    def translate(self):
        return self.value


