
class MysException(Exception):
    pass

class MysNotImplementedError(MysException):
    pass

class MysNotSupportedError(MysException):
    pass

class MysParamsTypeError(MysException):
    pass

class MysNotUrnFormatError(MysException):
    pass
