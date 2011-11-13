'''
Created on Nov 10, 2011

@author: Haak Saxberg, Jess Hester
'''
import abc

from model_exceptions import *

class Model(object):
	"""Abstract base class for universal model objects

	Keyword arguments:
	kwargs -- undetermined

	"""
	__metaclass__ = abc.ABCMeta
	
	@classmethod
	def create(cls, **kwargs):
		"""Creates an internal representation of a Model from kwargs"""
		raise NotImplementedError(u"Create not overridden")

	@classmethod
	def get(cls, key):
		"""Gets an instance of the model using a unique primary key"""
		raise NotImplementedError(u"Get not overridden")

	def get_interface(self):
		"""Returns an interface to the correct backend API"""
		raise NotImplementedError(u"Get interface not overridden")

	def put(self):
		"""Store this instance in the backend"""
		raise NotImplementedError(u"Put not overridden")

	def pk(self):
		"""Gets the primary key field's value for this model"""
		pks = []
		for key, val in self.__class__.__dict__:
			# only Fields can act as primary keys:
			if not isinstance(value, Field):
				continue
			
			if value._meta["pk"]:
				pks += [val]
		
		# make sure there's only ONE primary key
		if len(pks) > 1:
			raise RuntimeException(u"Too many primary keys for {}".format(self))

		return pks[0].value

	def __repr__(self):
		return u"QUI Model: {}".format(self.__name__)
