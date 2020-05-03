
from functools import wraps


def memoize(function):
    """Memoization decorator"""
    memo = {}

    @wraps(function)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))

        if key in memo:
            return memo[key]

        rv = function(*args, **kwargs)
        memo[key] = rv
        return rv
    return wrapper
