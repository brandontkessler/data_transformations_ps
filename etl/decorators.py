import os
from functools import wraps
import time

import pandas as pd

from .helpers import cached_dtypes, date_columns


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__} in {run_time:.4f} secs")
        return value
    return wrapper


def check_fys_is_int(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_fys = kwargs.get('fys')
        if isinstance(check_fys, int):
            kwargs['fys'] = [check_fys]
        return func(*args, **kwargs)
    return wrapper

def build_operator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = kwargs.get('data')
        threshold = kwargs.get('threshold')

        if data is None:
            data = args[0]

        if threshold is None:
            threshold = args[1]

        greater_than = kwargs.get('greater_than')
        equal_to = kwargs.get('equal_to')

        if greater_than and equal_to:
            mask = data.gift_plus_pledge >= threshold
        elif greater_than and not equal_to:
            mask = data.gift_plus_pledge > threshold
        elif not greater_than and equal_to:
            mask = data.gift_plus_pledge <= threshold
        elif not greater_than and not equal_to:
            mask = data.gift_plus_pledge < threshold
        else:
            raise Exception('There was an error building the operator')

        kwargs['mask'] = mask
        return func(*args, **kwargs)
    return wrapper


def cache_working_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        type = kwargs.get('type')

        if not os.path.exists('cache'):
            os.mkdir('cache')

        value.to_csv(f'cache/{type}_working.csv', index=False)
        print('saved working to cache')

        return value
    return wrapper


def check_working_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        type = kwargs.get('type')

        if os.path.exists(f'cache/{type}_working.csv'):
            print('reading from cache')
            data = pd.read_csv(f'cache/{type}_working.csv',
                dtype=cached_dtypes.get(type), parse_dates=date_columns.get(type))
            return data

        print('not found in cache')
        return func(*args, **kwargs)
    return wrapper
