#!/usr/bin/env python3
"""
web
"""
from functools import wraps
import redis
import requests
from typing import Callable


r = redis.Redis()


def count_visits(method: Callable) -> Callable:
    """
    cache the result of method with an
    expiration time of 10 seconds
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        wraps method and cachees it result
        """
        r.incr("count:{}".format(url))
        res = r.get("response:{}".format(url))
        if res:
            return res.decode("utf-8")
        res = method(url)
        # r.set("count:{}".format(url), 1)
        r.setex("response:{}".format(url), 10, res)
        return res
    return wrapper


def get_page(url: str) -> str:
    """
    Track how many times a particular URL
    was accessed in the key "count:{url}"
    """
    res = requests.get(url)
    return res.text