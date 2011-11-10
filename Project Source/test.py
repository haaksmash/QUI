from decorators import stored

class StrField(object):
    pass

class IntField(object):
    pass


@stored(db="mongodb", primary_key="unique_id")
class Tester(object):
    unique_id = 1
    def __init__(self, age):
        self.name = "Haak"
        self.age = age

    def __repr__(self):
        return u"{}".format(self.name)


class Tester2(object):
    unique_id = 3

@stored(primary_key="unique_id")
class Tester3(Tester2):
    pass