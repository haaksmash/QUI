'''
Created on Nov 13, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

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
    
    @abc.abstractmethod
    @classmethod
    def get(self, pk):
        pass
    
    @abc.abstractmethod
    @classmethod
    def create(cls, **kwargs):
        pass


    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        pass