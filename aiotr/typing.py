"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from typing import Callable, Optional, Union

from typing import Literal, TypedDict


class Request(TypedDict):
    method: str
    arguments: Optional[dict]
    tag: int


class Response(TypedDict):
    result: Union[Literal["success"], str]
    arguments: Optional[dict]
    tag: int


TagFactory = Callable[[], int]
