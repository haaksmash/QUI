'''
Created on Nov 10, 2011

@author: Haak Saxberg and Jess Hester
'''
import abc

from model_exceptions import *
from fields import Field

class Model(object):
	"""Abstract base class for universal model objects

	Keyword arguments:
	kwargs -- undetermined

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
	def get_interface(self):
		"""Returns an interface to the correct backend API"""
		raise NotImplementedError(u"Get interface not overridden")
	
	@abc.abstractmethod
	def put(self):
		"""Store this instance in the backend"""
		raise NotImplementedError(u"Put not overridden")
	
	#@abc.abstractmethod
	@property
	def pk(self):
		"""Gets the primary key field's value for this model"""
		pks = []
		for key, val in self.__class__.__dict__:
			# only Fields can act as primary keys:
			if not isinstance(val, Field):
				continue
			
			if val._meta["pk"]:
				pks += [val]
		
		# make sure there's only ONE primary key
		if len(pks) > 1:
			raise RuntimeError(u"Too many primary keys for {}".format(self))

		return pks[0].value

	def __repr__(self):
		return u"QUI Model: {}".format(self.__class__.__name__)


class ModelInstance():
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod
	def put(self):
		pass

	@abc.abstractmethod
	def delete(self):
		pass
	