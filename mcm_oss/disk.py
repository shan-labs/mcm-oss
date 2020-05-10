"""
Khinshan Khan - disk.py.
"""
from collections import deque

class Disk:
    """TODO"""
    def __init__(self, disks_max):
        self._disks = [deque() for i in range(disks_max)]
