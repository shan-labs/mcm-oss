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
        self._pid_count = 1

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
            print(self._memory)
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
                start = proc["start"] - 1
                end = proc["end"] + 1
                correspond_start = -1
                correspond_end = -1
                empty_keys = []
                for free_memory_block in self._memory.keys():
                    print(free_memory_block)
                    print(self._memory[free_memory_block])
                    if (correspond_start != -1 and correspond_end != -1):
                        break
                    if(start in self._memory[free_memory_block]["end"]):
                        find_start = self._memory[free_memory_block]["end"].index(start)
                        correspond_start = self._memory[free_memory_block]["start"][find_start]
                        self._memory[free_memory_block]["start"].pop(find_start)
                        self._memory[free_memory_block]["end"].pop(find_start)
                    if(end in self._memory[free_memory_block]["start"]):
                        find_end = self._memory[free_memory_block]["start"].index(end)
                        correspond_end = self._memory[free_memory_block]["end"][find_end]
                        self._memory[free_memory_block]["start"].pop(find_end)
                        self._memory[free_memory_block]["end"].pop(find_end)
                    if not self._memory[free_memory_block]["start"]:
                        empty_keys.append(free_memory_block)
                start = correspond_start if correspond_start != -1 else start + 1
                end = correspond_end if correspond_end != -1 else end - 1
                for empty_key in empty_keys:
                    self._memory.pop(empty_key, None)
                memory_range = end - start
                if memory_range not in self._memory and memory_range != 0:
                    self._memory[memory_range] = {"start": [], "end": []}
                    if memory_range != 0:
                        self._memory[memory_range]["start"].append(start)
                        self._memory[memory_range]["end"].append(end)
                        self._memory[memory_range]["start"].sort()
                        self._memory[memory_range]["end"].sort()

    def _create_pcb(self, command, size):
        """Determine process information using first fit contiguous memory, if possible."""
        proc_type = "RT" if command == "AR" else "Common"
        # first fit algorithm for memory
        # get all (if any) contiguous memory blocks with sufficient size
        free_memory_blocks = sorted(filter(lambda num: num >= size, self._memory.keys()))
        if(len(free_memory_blocks) < 1): # early exit if no contiguous memory blocks are available
            return None
        # pick the first possible 'bucket' per first fit approach
        free_memory_key = free_memory_blocks[0]
        memory_block = self._memory[free_memory_key]
        # figure out new process's information
        start = memory_block["start"][0]
        end = start + size - 1
        # rearrange memory per new usage
        memory_remainder = memory_block["end"][0] - end - 1
        self._memory[free_memory_key]["start"].pop(0)
        memory_remainder_end = self._memory[free_memory_key]["end"].pop(0)
        # pop key if no more ranges left for it
        if not self._memory[free_memory_key]["start"]:
            self._memory.pop(free_memory_key, None)
        # in the case the key didn't exist, give it default values
        if memory_remainder not in self._memory and memory_remainder != 0:
            self._memory[memory_remainder] = {"start": [], "end": []}
        # as long as the range isn't 0, we have usable contiguous memory
        if memory_remainder != 0:
            self._memory[memory_remainder]["start"].append(start + size)
            self._memory[memory_remainder]["end"].append(memory_remainder_end)
        # pcb for newly created process
        proc = {"type": proc_type, "pid": self._pid_count, "start": start, "end": end}
        self._pid_count += 1
        return proc
