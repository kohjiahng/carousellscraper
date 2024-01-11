class BufferPool:
    def __init__(self, max_length):
        self.pool = []
        self.max_length = max_length

    def add(self, item):
        if item in self.pool:
            return False
        self.pool.append(item)
        if len(self.pool) >= self.max_length:
            self.pool.pop(0)
        return True