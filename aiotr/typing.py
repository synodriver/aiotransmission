"""
Copyright (c) 2008-2024 synodriver <synodriver@gmail.com>
"""

from typing import Callable, Literal, Optional, TypedDict, Union


class Request(TypedDict):
    method: str
    arguments: Optional[dict]
    tag: int


class Response(TypedDict):
    result: Union[Literal["success"], str]
    arguments: Optional[dict]
    tag: int


TagFactory = Callable[[], int]
