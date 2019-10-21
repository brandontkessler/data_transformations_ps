from functools import wraps

def check_fys_is_int(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_fys = kwargs.get('fys')
        if isinstance(check_fys, int):
            kwargs['fys'] = [check_fys]
        return func(*args, **kwargs)
    return wrapper
