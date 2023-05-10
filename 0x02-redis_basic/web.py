#!/usr/bin/env python3
"""
web
"""
from functools import wraps
from typing import Callable
import redis
import requests


r = redis.Redis()
"""Global redis instance"""


def count_url(method: Callable) -> Callable:
    """
    cache the result of method with an
    expiration time of 10 seconds
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        wraps method and cachees it result
        """
        r.incrby(f"count:{url}", 1)
        # res = r.get(f"response:{url}")
        # if res:
        #     return res.decode("utf-8")
        res = method(url)
        # r.set(f"count:{url}", 0)
        # r.setex(f"response:{url}", 10, res)
        r.expire(f"count:{url}", 10)
        return res
    return wrapper


@count_url
def get_page(url: str) -> str:
    """
    Track how many times a particular URL
    was accessed in the key "count:{url}"
    """
    res = requests.get(url)
    return res.text
