'''
@author: Haak Saxberg and Jess Hester

This mixin simply employs Python's pickling abilities. Model instances
are stored in a directory for that model (inside of the QUI directory), 
and can be gotten from the same place.
'''
from fields import Field
from modelmixins import ModelMixin
from fieldmixins import FieldMixin

from quiexceptions.model_exceptions import *

import os,pickle,abc

class PickleModelMix(ModelMixin):
    # Default port, won't really matter
    _port = 0
    
    #default path is current directory
    _path = os.getcwd()
    
    def __getstate__(self):
        """ Returns a dictionary representing the state of the model """
        global AutoSub
        AutoSub = self.__class__
        return (self.__dict__, self.__class__)
    
    def put(self):
        """ Take the model instance and store it in a file
            under ModelName/self.id (to make sure the file name
            is unique)
        """
        # pickle instances into folders by class name, and files by pk
        dirname = self.__class__.__name__
        if not os.path.exists(dirname):
            print "making new directory...{}".format(dirname)
            os.makedirs(dirname)
        else:
            print "found directory: {}".format(dirname)
            
        # if this is a pk'd model, we know what to do
        if self.pk:
            filename = os.path.join(dirname,str(self.pk))
        else:
            flist = [ x for x in os.listdir("{}\\{}".format(self._path, dirname)) if x[0] not in ['.',]]
            print flist
            if len(flist) > 0:
                m = max(map(lambda x: int(x), flist))
                self._id = m + 1
            else:
                self._id = 1
            filename = os.path.join(dirname,str(self.pk))
        
        # since we can't pickle dynamically created classes without a *lot* of pain,
        # pickle a dict that describes the class.
        # Added benefit: can load into other classes, if necessary. Great for porting!
        f = open(filename,"w")
        pickle.dump(self._get_interface(), f)
        f.close()
    
    @classmethod        
    def get(cls, **kwargs):
        if kwargs.has_key("pk"):
            dirname = "{}\\{}".format(cls._path, cls.__name__)
            if not os.path.exists(dirname):
                raise ObjectDoesNotExist("Could not find any stored {}".format(dirname))
            
            filename = os.path.join(dirname,str(kwargs['pk']))
            
            f = open(filename,"r")
            storedclass = pickle.load(f)
            f.close()
            
            # maybe a little janky, but this seems pretty elegant to me
            return cls.create(**storedclass)
        else:
            raise NoPrimaryKey("No {} with primary key {}".format(cls.__name__,kwargs['pk']))
        
    @classmethod
    def create(cls, **kwargs):
        # if they have special constructor arguments...
        if kwargs.has_key("init_args"):
            x = cls(**kwargs["init_args"])
            x._init_args = kwargs['init_args']
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
    
    def _get_interface(self):
        """ Gets the representation in a Json object """
        json = {}
        for key in dir(self):
            # skip private and special members
            if key[0] == "_" and (key != "_{}__id".format(self.__class__.__name__) and key != "_id"):
                continue

            if hasattr(getattr(self, key), "__call__"):
                # some fields may eventually be callable - catch their values.
                if isinstance(getattr(self, key), Field):
                    value = getattr(self,key).value
                else:
                # skip non-field callables
                    continue
            # is this a field?
            if key in self._field_names.keys():
                f = self._get_direct(key)
                value = f.translate()
            
            value = getattr(self, key)
            json.update({key:value})
        
        return json
    
class PickleFieldMix(FieldMixin): 
    def clean(self):
        """ Not currently implemented """
        pass
    
    def translate(self):
        """ Returns the field's value """
        return self.value