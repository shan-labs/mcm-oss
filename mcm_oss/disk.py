"""
Khinshan Khan - disk.py.

This module implements HDD simulation with FCFS per disk management.
"""
from collections import deque
import itertools


class Disk:
    """Enclosed disk management"""
    def __init__(self, disks_max):
        self._disk_num = disks_max - 1
        self._disks = [deque() for i in range(disks_max)]

    def io_snapshot(self):
        """Print all processes' across all disks in relation to disk."""
        for index, disk in enumerate(self._disks, start=0):
            procs = iter(disk)
            running = next(procs, None)
            if running:
                print(running["pid"], index, "serving", sep='\t')
            for proc in procs:
                print(proc["pid"], index, "waiting", sep='\t')

    def memory_snapshot(self):
        """Print all processes' memory across all disks."""
        for proc in itertools.chain(*self._disks):
            print(proc["type"], proc["start"], proc["end"], sep='\t')

    def add_proc(self, disk_num, proc):
        """Adds a process to disk."""
        if disk_num < 0 or disk_num > self._disk_num:
            print("That disk doesn't exist!")
        else:
            self._disks[disk_num].append(proc)

    def remove_proc(self, disk_num):
        """Removes a process from disk if possible."""
        if disk_num < 0 or disk_num > self._disk_num:
            print("That disk doesn't exist!")
            return None
        elif not self._disks[disk_num]:
            return None
        else:
            return self._disks[disk_num].popleft()
