"""
Khinshan Khan - cli.py.
"""
from collections import deque
import itertools

from mcm_oss import memory
from mcm_oss import disk


class OSS:
    """An OS mimicker."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self, ram_max, disks_max):
        self._memory = memory.Memory(ram_max)
        self._num_of_disks = disk.Disk(disks_max)
        self._rt_ready_queue = deque()
        self._common_ready_queue = deque()
        self._pid_count = 1

    def process(self, command, size):
        proc = self._create_pcb(command, int(size))
        if (proc == None): # short circuit if bad size
            return
        if(command == 'AR'):
            self._rt_ready_queue.append(proc)
        elif(command == 'A'):
            self._common_ready_queue.append(proc)

    def hard_disk(self, command, number):
        if(command == 'd'):
            pass
        elif(command == 'D'):
            pass
        print('hard disk', command, number)

    def show(self, show_type):
        """TODO: WIP, currently just debug prints"""
        if(show_type == 'r'):
            print("PID", "TYPE", "STATUS", sep='\t')
            procs = itertools.chain(self._rt_ready_queue, self._common_ready_queue)
            running = next(procs, None)
            if running:
                print(running["pid"], running["type"], "running", sep='\t')
            for proc in procs:
                print(proc["pid"], proc["type"], "waiting", sep='\t')
        elif(show_type == 'i'):
            # TODO: print IO info
            print(self._memory._memory)
        elif(show_type == 'm'):
            print("TYPE", "M_START", "M_END", sep='\t')
            procs = itertools.chain(self._rt_ready_queue, self._common_ready_queue)
            for proc in procs:
                print(proc["type"], proc["start"], proc["end"], sep='\t')

    def time(self, command):
        if(command == 'Q'):
            if self._rt_ready_queue:
                self._rt_ready_queue.rotate(-1)
            elif self._common_ready_queue:
                self._common_ready_queue.rotate(-1)
        elif(command == 't'):
            proc = None
            if self._rt_ready_queue:
                proc = self._rt_ready_queue.popleft()
            elif self._common_ready_queue:
                proc = self._common_ready_queue.popleft()
            if proc:
                self._memory.restore_memory(proc["start"], proc["end"])

    def _create_pcb(self, command, size):
        """Determine process information using first fit contiguous memory, if possible."""
        if(size == 0):
            print("Can't have a process of size 0.")
            return None
        start, end = self._memory.find_free(size)
        if start == None:
            print("Not enough contiguous memory available for this process.")
            return None
        # pcb for newly created process
        proc_type = "RT" if command == "AR" else "Common"
        proc = {"type": proc_type, "pid": self._pid_count, "start": start, "end": end}
        self._pid_count += 1
        return proc
