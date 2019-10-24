from functools import wraps

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
