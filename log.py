def logging(function):
    def decorated_function(*args, **kwargs):
        a = function(*args, **kwargs)
        # print(function.__name__, 'in:', (*args, kwargs), 'return: ', a)
        return a
    return decorated_function

