def print_result_decorator(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f"{func.__name__} : {ret}")
        return ret
    return wrapper

def function_name_decorator(func, *args, **kwargs):
    def wrapper(func):
        function_name = func.__name__
        ret = func(function_name=function_name, *args, **kwargs)
        return ret
    return wrapper
