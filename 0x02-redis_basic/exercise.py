#!/usr/bin/env python3
"""
exercise
"""
from functools import wraps
import redis
import uuid
from typing import Callable, Optional, Union
AllowedTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """ Counts how many times methods is called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for methods call calls"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs
    for a particular function
    """
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """Wrapper function for methids call history"""
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """ display the history of calls of a particular function """
    db = redis.Redis()
    func_name = method.__qualname__
    calls_counts = db.get(func_name)
    print("{} was called {} times:".format(func_name, calls_counts))
    input_list = func_name + ":inputs"
    output_list = func_name + ":outputs"
    inputs = db.lrange(input_list, 0, -1)
    outputs = db.lrange(output_list, 0, -1)
    pairs = zip(inputs, outputs)
    for pair in pairs:
        print("{}(*{}) -> {}".format(func_name, pair[0].decode(),
                                     pair[1].decode()))


class Cache:
    """ Creates a new instance of Cache """
    def __init__(self):
        """ Initiates a new instance of cache """
        self._redis = redis.Redis()
        self._redis.flushdb

    @count_calls
    @call_history
    def store(self, data: AllowedTypes) -> str:
        """
        Takes a data argument and returns a string.
        The method should generate a random key
        (e.g. using uuid), store the input data in
        Redis using the random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> AllowedTypes:
        """
        Take a key string argument and an optional
        Callable argument named fn. This callable will
        be used to convert the data back to the desired format
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key) -> str:
        """get key value as str"""
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """get key value as int"""
        return self.get(key, fn=int)
