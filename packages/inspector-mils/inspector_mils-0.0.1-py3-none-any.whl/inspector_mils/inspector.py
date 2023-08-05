"""
inspector-mils/inspector.py
"""
from functools import wraps
from datetime import datetime


def inspect(func):
    """
    inspect
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        wrapper
        """

        print(f'[{str(datetime.now())}] Starting inspect..')
        print(f'[{str(datetime.now())}] {func.__name__}() called..')
        print(f'[{str(datetime.now())}] args: {args}')
        print(f'[{str(datetime.now())}] kwargs: {kwargs}')
        print(f'[{str(datetime.now())}] Ending inspect..')

        return func(*args, **kwargs)
    return wrapper
