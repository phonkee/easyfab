from functools import wraps

import fabric.api


def ensure_use_deployment(func):
    """ Wrapper which checks whether set_language was called
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not fabric.api.env.get('__deployment'):
            fabric.api.abort('Run set_deployment first')
        return func(*args, **kwargs)
    return wrapper


def easyfabtask(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    setattr(wrapper, '__easyfabtask', True)
    return wrapper
