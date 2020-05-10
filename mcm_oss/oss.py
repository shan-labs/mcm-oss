from collections import deque
import itertools

class OSS:
    """An OS mimicker."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self, ram_max, disks_max):
        self.memory = {ram_max: {"start": [0], "end": [ram_max]}}
        self._num_of_disks = disks_max
        self._rt_ready_queue = deque()
        self._common_ready_queue = deque()
        self.pid_count = 1

    def process(self, command, size):
        proc = self._create_pcb(command, int(size))
        if (proc == None): # short circuit if not enough
            print("Not enough contiguous memory available for this process.")
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
            print(self.memory)
        elif(show_type == 'm'):
            print("TYPE", "M_START", "M_END", sep='\t')
            procs = itertools.chain(self._rt_ready_queue, self._common_ready_queue)
            for proc in procs:
                print(proc["type"], proc["start"], proc["end"], sep='\t')

    def time(self, command):
        pass

    def _create_pcb(self, command, size):
        """Determine process information using first fit contiguous memory, if possible."""
        proc_type = "RT" if command == "AR" else "Common"
        # first fit algorithm for memory

        # get all (if any) contiguous memory blocks with sufficient size
        free_memory = sorted(filter(lambda num: num >= size, self.memory.keys()))
        if(len(free_memory) < 1): # early exit if no contiguous memory blocks are available
            return None
        # pick the first possible 'bucket' per first fit approach
        free_memory_key = free_memory[0]
        memory_block = self.memory[free_memory_key]
        # figure out new process's information
        start = memory_block["start"][0]
        end = start + size - 1
        # rearrange memory per new usage
        memory_remainder = memory_block["end"][0] - end - 1
        self.memory[free_memory_key]["start"].pop(0)
        memory_remainder_end = self.memory[free_memory_key]["end"].pop(0)
        # pop key if no more ranges left for it
        if not self.memory[free_memory_key]["start"]:
            self.memory.pop(free_memory_key, None)
        # in the case the key didn't exist, give it default values
        if memory_remainder not in self.memory and memory_remainder != 0:
            self.memory[memory_remainder] = {"start": [], "end": []}
        # as long as the range isn't 0, we have usable contiguous memory
        if memory_remainder != 0:
            self.memory[memory_remainder]["start"].append(start + size)
            self.memory[memory_remainder]["end"].append(memory_remainder_end)
        # pcb for newly created process
        proc = {"type": proc_type, "pid": self.pid_count, "start": start, "end": end}
        self.pid_count += 1
        return proc
