import time


def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    return result, time.time() - start_time
