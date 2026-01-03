from collections import deque

class PhysicalMemoryManager:
    def __init__(self, total_blocks=1024, block_size=16):
        self.block_size = block_size
        self.total_blocks = total_blocks
        self.free_blocks = deque(range(total_blocks))
        self.mapping_table = {}

    def allocate(self, rid, seq_len):
        # 預計需要塊數 (Prompt + 預留生成空間)
        needed = (seq_len + 32 + self.block_size - 1) // self.block_size
        if len(self.free_blocks) < needed:
            return False
        self.mapping_table[rid] = [self.free_blocks.popleft() for _ in range(needed)]
        return True

    def deallocate(self, rid):
        if rid in self.mapping_table:
            blocks = self.mapping_table.pop(rid)
            self.free_blocks.extend(blocks)

    def get_usage_ratio(self):
        return (self.total_blocks - len(self.free_blocks)) / self.total_blocks