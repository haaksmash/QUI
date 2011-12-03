class QUIException(Exception):
    pass

class QUIModelException(QUIException):
    pass

class QUIFieldException(QUIException):
    pass


class DNEException(QUIException):
    pass