import time
from contextlib import contextmanager

@contextmanager
def log_time(label="op"):
    start = time.time()
    try:
        yield
    finally:
        print(f"{label} took {time.time()-start:.3f}s")
