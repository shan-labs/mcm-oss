"""
Khinshan Khan - memory.py.
"""


class Memory:
    """First fit contiguous memory management."""
    def __init__(self, ram_max):
        self._memory = {ram_max: {"start": [0], "end": [ram_max]}}

    def find_free(self, size):
        # first fit algorithm for memory
        # get all (if any) contiguous memory blocks with sufficient size
        free_memory_blocks = sorted(filter(lambda num: num >= size, self._memory.keys()))
        if(len(free_memory_blocks) < 1):  # early exit if no contiguous memory blocks are available
            return (None, None)
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
        return (start, end)

    def restore_memory(self, start, end):
        start = start - 1
        end = end + 1
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
