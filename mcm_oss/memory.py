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
            if free_range not in self._memory:
                self._memory[free_range] = {"start": [], "end": []}
            self._memory[free_range]["start"].append(block_start)
            self._memory[free_range]["end"].append(block_end)
        return (start, end)

    def restore_memory(self, start, end):
        pass
