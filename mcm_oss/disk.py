"""
Khinshan Khan - disk.py.
"""
from collections import deque

class Disk:
    """TODO"""
    def __init__(self, disks_max):
        self._disks = [deque() for i in range(disks_max)]

    def snapshot(self):
        for index, disk in enumerate(self._disks, start=0):
            print(index, disk)

    def add_proc(self, proc, disk_num):
        self._disks[disk_num].append(proc)

    def remove_proc(self, disk_num):
        if self._disks[disk_num]:
            return self._disks[disk_num].popleft()
        else:
            return None
