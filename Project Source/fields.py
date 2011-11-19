'''
Created on Nov 10, 2011

@author: Haak Saxberg and Jess Hester
'''
import warnings
import datetime
import re
import abc


from decorators import OProperty

from validators import *

class FieldDNE(Exception):
    pass

class ValidationError(ValueError):
    pass

class Field(object):
    """Abstract base class for universal field objects (UFOs)
        
    Keyword arguments: 
    kwargs -- as yet undetermined
    
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_python(self, value):
        """Converts field objects from internal representation to Python data types"""
        raise NotImplementedError("to_python not overriden")

    @abc.abstractmethod
    def getvalue(self):
        """Field value as a Python datatype. Calls to_python"""
        raise NotImplementedError("Value getter not overriden")

    @abc.abstractmethod
    def setvalue(self, val):
        """Sets the value; converts from a Python datatype to an internal representation"""
        raise NotImplementedError("Value setter not overriden")

    def delvalue(self):
        """Deletes this field's value"""
        raise warnings.warn("No way to delete field values",Warning)
    value = OProperty(getvalue, setvalue, delvalue, "value of this field")

    def validate(self, val):
        """Ensures Python datatype/internal representation translation is valid"""
        for validator in self._validators:
            validator(val)

        return True
    
    @abc.abstractmethod
    def clean(self):
        """Sanitizes the data before carrying out operations"""
        raise NotImplementedError("Sanitation not implemented")
    
    @abc.abstractmethod    
    def translate(self):
        """The actual translation from our Python representation to backend-readable representation"""
        raise NotImplementedError("Translation not implemented")

    def __init__(self, *args, **kwargs):
        self._validators = ()
        self._value = None
        if kwargs.has_key("primary_key"):
            self._primary_key = True
        else:
            self._primary_key = False
            
        


class StringField(Field):
    """ """
    def to_python(self, value):
        """Converts from intermediate StringField representation to Python string"""
        if value is None: 
            return value
        return unicode(value)

    def setvalue(self, val):
        """Takes a string and stores it as a StringField"""
        if self.validate(val):
            self._value = val

    def getvalue(self):
        """Return the string representation of the StringField"""
        return self.to_python(self._value)

    def delvalue(self):
        """Sets value of StringField to None"""
        self._value = None

    def validate(self, val):
        """Ensures value is a properly formatted string"""
        #TODO: add keyword activated validators
        try:
            self._value = str(self._value)
        except Exception:
            raise ValidationError(r"Could not convert to string: {}".format(self._value))
        
        return super(StringField, self).validate(val)
    
    def __init__(self, *args, **kwargs):
        print "StringField's init"
        super(StringField, self).__init__(*args, **kwargs)

class IntegerField(Field):
    """Class for Intergers"""
    def to_python(self, value):
        if value is None: 
            return value
        return int(value)

    def setvalue(self, val):
        """Takes an int and stores it as an IntegerField"""
        if self.validate(val):
            self._value = val 

    def getvalue(self):
        return self.to_python(self._value)

    def delvalue(self):
        self._value=None

    def validate(self, val):
        try:
            self._value = int(self._value)
        except Exception, e:
            raise ValidationError(r"Could not convert to int: {}".format(self._value))
        
        return super(IntegerField, self).validate(val)
    
    def __init__(self, *args, **kwargs):
        print "IntegerField's init"
        super(IntegerField, self).__init__(*args, **kwargs)

class FloatField(Field):
    def to_python(self, value):
        if value is None:
            return value
        return float(value)

    def setvalue(self, val):
        if self.validate(val):
            self._value = val 

    def getvalue(self):
        return self.to_python(self._value)

    def delvalue(self):
        self._value = None

    def validate(self, val):
        try:
            self._value = float(self._value)
        except Exception, e:
            raise ValidationError(r"Could not convert to float: {}".format(self._value))
        
        return super(FloatField, self).validate(val)

class BooleanField(Field):
    def to_python(self, value):
        if value is None:
            return value
        return bool(value)

    def setvalue(self, val):
        if self.validate(val):
            self._value = val 

    def getvalue(self):
        return self.to_python(self._value)

    def delvalue(self):
        self._value = None

    def validate(self, val):
        try:
            value = bool(val)
        except Exception, e:
            raise ValidationError(r"Could not convert to boolean: {}".format(self._value))
        
        return super(BooleanField, self).validate(val)
        

class DateField(Field):
    ansi_date_re = re.compile(r'^\d{1,2}-\d{1,2}-\d{4}$')

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, int):
            return datetime.datetime.utcfromtimestamp(value).date()
        try:
            return datetime.datetime.strptime(value, "%d/%m/%Y").date()
        except:
            # Now that we have the date string in YYYY-MM-DD format, check to make
            # sure it's a valid date.
            # We could use time.strptime here and catch errors, but datetime.date
            # produces much friendlier error messages.
            day, month, year = map(int, value.split('-'))
            try:
                return datetime.date(year, month, day)
            except ValueError, e:
                msg = self.error_messages['invalid_date'] % _(str(e))
                raise ValidationError(msg)

    def setvalue(self, val):
        if self.validate(val):
            self._value = val 
        
    def getvalue(self):
        return self.to_python(self._value)

    def delvalue(self):
        self._value = None

    def validate(self, val):
        if isinstance(val, str):
            try:
                datetime.datetime.strptime(val, "%d/%m/%Y").date()
            except ValueError, e:
                raise ValidationError(r"Couldn't coerce into a date: {}".format(val))
        elif isinstance(val, int):
            try:
                datetime.datetime.utcfromtimestamp(val).date()
            except ValueError, e:
                raise ValidationError(r"Not a valid timestamp: {}".format(val))
        elif not ansi_date_re.search(val):
            raise ValidationError("Not a valid date: {}".format(val))
        else:
            raise ValidationError(r"Could not create a date object: {}".format(val))

        return super(DateField, self).validate(val)
