import time
from typing import Optional


def get_current_time():
    return int(time.time() * 1000)


def is_timeout(time: Optional[int], threshold: int):
    return time and get_current_time() - time > threshold
