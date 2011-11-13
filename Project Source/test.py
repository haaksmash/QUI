from decorators import *

class StrField(object):
    pass

class IntField(object):
    pass


@stored_direct(db="mongodb", primary_key="unique_id")
class Tester(object):
    unique_id = 1
    def __init__(self, age):
        self.name = "Haak"
        self.age = age

    def __repr__(self):
        return u"{}".format(self.name)

@stored_mixin
class Tester2(object):
    unique_id = 3
    def reveal(self):
        print "not overwritten"
        
@stored_mixin(db="simpledb")        
class Tester3(object):
    pass