from collections import deque

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
            print('time', self.memory)
        elif(show_type == 'i'):
            print(self._rt_ready_queue)
            print(self._common_ready_queue)
        elif(show_type == 'm'):
            print(self.memory)

    def time(self, command):
        pass

    def _create_pcb(self, command, size):
        """Determine process information using first fit contiguous memory, if possible."""
        proc_type = "Real-Time" if command == "AR" else "Common"
        # first fit algorithm for memory
        print(self.memory.keys())
        free_memory = sorted(filter(lambda num: num >= size, self.memory.keys()))
        if(len(free_memory) < 1):
            return None
        memory_block = self.memory[free_memory[0]]
        start = memory_block["start"][0]
        end = start + size - 1
        memory_remainder = memory_block["end"][0] - end - 1
        self.memory[free_memory[0]]["start"].pop()
        memory_remainder_end = self.memory[free_memory[0]]["end"].pop()
        if not self.memory[free_memory[0]]["start"]:
            self.memory.pop(free_memory[0], None)
        if memory_remainder not in self.memory and memory_remainder != 0:
            self.memory[memory_remainder] = {"start": [], "end": []}
        if memory_remainder != 0:
            self.memory[memory_remainder]["start"].append(start + size)
            self.memory[memory_remainder]["end"].append(memory_remainder_end)
        # pcb for newly created process
        proc = {"type": proc_type, "start": start, "end": end}
        return proc
