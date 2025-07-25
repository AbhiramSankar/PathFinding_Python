import time

def timer(func):
    """Decorator to print execution time of a function."""
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return res
    return wrapper
