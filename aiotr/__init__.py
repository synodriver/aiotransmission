"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
# spec see https://github.com/transmission/transmission/blob/master/extras/rpc-spec.txt
# config https://github.com/transmission/transmission/wiki/Editing-Configuration-Files
from aiotr.client import TransmissionClient
from aiotr.exception import (
    BaseTransmissionException,
    TransmissionConnectException,
    TransmissionException,
    TransmissionMisdirectedException,
    TransmissionUnauthorizedException,
)

__version__ = "0.1.1"
