"""
Copyright (c) 2008-2024 synodriver <synodriver@gmail.com>
"""

import json
import sys

DEFAULT_JSON_DECODER = json.loads
DEFAULT_JSON_ENCODER = json.dumps

DEFAULT_HOST = "http://127.0.0.1:9091/transmission/rpc"
DEFAULT_TIMEOUT = 30.0


class TagGen:
    def __init__(self):
        self._id = 1

    def __call__(self) -> int:
        self._id = (self._id + 1) % sys.maxsize
        return self._id
