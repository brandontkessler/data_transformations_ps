from functools import wraps
import time

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


def check_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Use data=self.data if not providing a dataset (self is args[0])
        if kwargs.get('data') is None:
            kwargs['data'] = args[0].data
        return func(*args, **kwargs)
    return wrapper


def check_series(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        options = ['Classics', 'Pops','Family', 'Summer', 'Specials',
                   'Connections', 'Organ', 'Chamber']

        if kwargs.get('series') is not None:
            check = all([s in options for s in kwargs['series']])
            msg = f'Series must only include: {options}'
            if not check:
                raise ValueError(msg)

        return func(*args, **kwargs)
    return wrapper


def inplace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        if kwargs.get('inplace') is True:
            args[0].data = val
        else:
            return val
    return wrapper
