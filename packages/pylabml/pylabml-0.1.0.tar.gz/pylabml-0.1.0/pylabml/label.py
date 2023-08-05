import functools

import pandas as pd
from .labeller import register


def labeller(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> pd.Series:
        return func(*args, **kwargs)
    register(func)
    return wrapper
