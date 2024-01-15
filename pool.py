class BufferPool:
    def __init__(self, max_length):
        self.pool = []
        self.max_length = max_length

    def check(self, item):
        return item not in self.pool
    
    def add(self, item):
        self.pool.append(item)
        if len(self.pool) >= self.max_length:
            self.pool.pop(0)