"""
Khinshan Khan - disk.py.
"""
from collections import deque
import itertools


class Disk:
    """TODO"""
    def __init__(self, disks_max):
        self._disks = [deque() for i in range(disks_max)]

    def io_snapshot(self):
        for index, disk in enumerate(self._disks, start=0):
            procs = iter(disk)
            running = next(procs, None)
            if running:
                print(running["pid"], index, "serving", sep='\t')
            for proc in procs:
                print(proc["pid"], index, "waiting", sep='\t')

    def memory_snapshot(self):
        for proc in itertools.chain(*self._disks):
            print(proc["type"], proc["start"], proc["end"], sep='\t')

    def add_proc(self, proc, disk_num):
        self._disks[disk_num].append(proc)

    def remove_proc(self, disk_num):
        if self._disks[disk_num]:
            return self._disks[disk_num].popleft()
        else:
            return None
