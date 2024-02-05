from time import time
def time_func(f: callable):
    """
    decorator to time a function duration.

    Usage:
    @time_func
    def my_function():
        pass
    
    my_function()

    Args:
        f (callable): function to time, which can be a generator function, async function, or normal function.
    
    Returns:
        callable: decorated function with time duration printed.
    """
    def inner(*args, **kwargs):
        start = time()
        r = f(*args, **kwargs)
        end = time()
        duration = end - start
        # Get name of callable:
        # https://stackoverflow.com/questions/33576932/do-all-callables-have-name/33578357#33578357
        print("="*20)
        print(f"executed: {getattr(f, '__name__', repr(f))}() python function")
        print(f"walltime: {duration} in secs.")
        print("="*20)
        return r
    return inner