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
#from google.appengine.api import apiproxy_stub_map
#from google.appengine.api import datastore_file_stub
from google.appengine.api import datastore
#from google.appengine.api import capabilities
#from google.appengine.api import datastore_errors
#from google.appengine.api import datastore_types
#from google.appengine.datastore import datastore_pb
#from google.appengine.datastore import datastore_query
#from google.appengine.datastore import datastore_rpc
#from google.appengine.datastore import entity_pb

class AppEngineModelMix(ModelMixin):
    _port = 8080
    _app_id = 'helloworld'
    os.environ['APPLICATION_ID'] = _app_id
    
#    datastore_file = os.path.join(os.path.dirname(__file__),'data')
#    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
#    stub = datastore_file_stub.DatastoreFileStub(_app_id, datastore_file, '/')
#    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
        
    def put(self):
        newSelf = self._get_interface()
        newSelf.put()
        
#        datastore._GetConnection()
        print "Putting to AppEngine at {}:{}".format(self._host, self._port)
#        request = datastore_pb.PutRequest()
#        request.entity_.append(datastore_pb.EntityProto("String",self._get_interface(),_app=self._app_id))
##        pathel = key.mutable_path().add_element()
##        pathel.set_type('FileModel')
##        pathel.set_name('test')
#        response = datastore_pb.PutResponse()
#        apiproxy_stub_map.MakeSyncCall('datastore_v3', 'Put', request, response)
#        return str(response)
#        datastore.Put(datastore.Entity("String",_app=self._app_id,unindexed_properties=self._get_interface()))
        
    def _get_interface(self):
        x = {}
        for el in dir(self):
            # skip private and special members
            if "_" == el[0]:
                continue
            # don't worry about callables
            if hasattr(getattr(self, el), "__call__"):
                continue
            # These are fields; add them to the interface.
            x[el] = getattr(self, el)
               
        # Create an Entity which we'll use to fill up our instance
        ent = datastore.Entity(self.__class__.__name__)
        # Create an appengine Model we'll actually fill with our fields
        newX = db.Model()
        newX._entity = ent
        newX._properties = x
        for key in x:
            newX._Model__set_property(ent,key,x[key])
        return newX
    
    @classmethod
    def get(cls, **kwargs):
        print "Getting from AppEngine"
#        request = datastore_pb.GetRequest()
#        key = request.add_key()
#        key.set_app(os.environ['APPLICATION_ID'])
#        pathel = key.mutable_path().add_element()
#        pathel.set_type('TestKind')
#        pathel.set_name('test')
#        response = datastore_pb.GetResponse()
#        apiproxy_stub_map.MakeSyncCall('datastore_v3', 'Get', request, response)
#        return str(response)
  
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


class AppEngineFieldMix(FieldMixin):
    def clean(self):
        pass
    
    def translate(self):
        return self.value


