"""
Khinshan Khan - memory.py.
"""


class Memory:
    """First fit contiguous memory management."""
    def __init__(self, ram_max):
        self._memory = {ram_max: {"start": [0], "end": [ram_max - 1]}}

    def find_free(self, size):
        # get all (if any) contiguous memory blocks with sufficient size
        free_memory_blocks = sorted(filter(lambda num: num >= size, self._memory.keys()))
        if not free_memory_blocks:  # early exit if no contiguous memory blocks are available
            return (None, None)
        # get the first available block's start and end for our new process's use
        memory_key = free_memory_blocks[0]
        start = self._memory[memory_key]["start"].pop(0)
        block_end = self._memory[memory_key]["end"].pop(0)
        # pop key if no more ranges left for it
        if not self._memory[memory_key]["start"]:
            self._memory.pop(memory_key, None)
        end = start + size - 1  # -1 since memory is inclusive (eg 0-99 is 100)
        if end != block_end:  # check if we're out of memory
            block_start = end + 1
            free_range = block_end - block_start + 1  # +1 due to inclusivity
            # in the case the key didn't exist, give it default values
            if free_range not in self._memory:
                self._memory[free_range] = {"start": [], "end": []}
            # add the remaining free block after process would be created
            self._memory[free_range]["start"].append(block_start)
            self._memory[free_range]["end"].append(block_end)
        return (start, end)

    def restore_memory(self, start, end):
        search_start = start - 1  # the value of start we want to search for, since it'll 'connect'
        search_end = end + 1  # the value of end we want to search for, since it'll 'connect'
        found_start = -1  # if a 'connecting' start is found, store it here
        found_end = -1  # if a 'connecting' end is found, store it here
        empty_keys = []  # any keys that need to be removed from `self._memory'
        for free_memory_block in self._memory.keys():
            if (found_start != -1 and found_end != -1):  # done at this point, no need to continue
                break
            if(search_start in self._memory[free_memory_block]["end"]):
                find_start = self._memory[free_memory_block]["end"].index(search_start)
                found_start = self._memory[free_memory_block]["start"][find_start]
                self._memory[free_memory_block]["start"].pop(find_start)
                self._memory[free_memory_block]["end"].pop(find_start)
            if(search_end in self._memory[free_memory_block]["start"]):
                find_end = self._memory[free_memory_block]["start"].index(search_end)
                found_end = self._memory[free_memory_block]["end"][find_end]
                self._memory[free_memory_block]["start"].pop(find_end)
                self._memory[free_memory_block]["end"].pop(find_end)
            if not self._memory[free_memory_block]["start"]:
                empty_keys.append(free_memory_block)  # can't pop key during the loop, save for exit
        for empty_key in empty_keys:
            self._memory.pop(empty_key, None)
        # determine free block's ranges
        start = found_start if found_start != -1 else search_start + 1
        end = found_end if found_end != -1 else search_end - 1
        free_range = end - start + 1  # +1 due to inclusivity
        # in the case the key didn't exist, give it default values
        if free_range not in self._memory:
            self._memory[free_range] = {"start": [], "end": []}
        # add the newly freed memory ranges to memory
        self._memory[free_range]["start"].append(start)
        self._memory[free_range]["end"].append(end)
        # sort to ensure first fit algorithm when finding free actually gets 'first' block available
        self._memory[free_range]["start"].sort()
        self._memory[free_range]["end"].sort()
