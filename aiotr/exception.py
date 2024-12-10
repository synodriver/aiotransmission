"""
Copyright (c) 2008-2024 synodriver <synodriver@gmail.com>
"""


class BaseTransmissionException(Exception):
    """
    transmission errors
    """

    pass


class TransmissionException(BaseTransmissionException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)


class TransmissionConnectException(BaseTransmissionException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)


class TransmissionMisdirectedException(BaseTransmissionException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class TransmissionUnauthorizedException(BaseTransmissionException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg
