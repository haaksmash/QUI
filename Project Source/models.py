'''
Created on Nov 10, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

from model_exceptions import *
from fields import Field

class Model(object):
	"""Abstract base class for universal model objects

	This class defines the interface for all stored models; anything that
	aspires to be a QUI model has to satisfy these abstract methods.
	"""
	__metaclass__ = abc.ABCMeta
	
	@classmethod
	@abc.abstractmethod
	def create(cls, **kwargs):
		"""Creates an internal representation of a Model from kwargs"""
		raise NotImplementedError(u"Create not overridden")
	
	@classmethod
	@abc.abstractmethod
	def get(cls, key):
		"""Gets an instance of the model using a unique primary key"""
		raise NotImplementedError(u"Get not overridden")
	
	@abc.abstractmethod
	def _get_interface(self):
		"""Returns an interface to the correct backend API"""
		raise NotImplementedError(u"Get interface not overridden")
	
	@abc.abstractmethod
	def put(self):
		"""Store this instance in the backend"""
		raise NotImplementedError(u"Put not overridden")
	
	#@abc.abstractmethod
	@property
	def pk(self):
		#Gets the primary key field's value for this model
		try:
			return getattr(self, self._pk_name)
		except:
			return None
	
	
	@property
	def _pk_name(self):
		return "_id"
	
	def __repr__(self):
		return u"<QUI Model: {}>".format(self.__class__.__name__)