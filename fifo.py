
class fifo:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
    
    def remove(self, item):
        self.queue.remove(item)

    def checkWhoCameFirst(self, item):
        theFirst = 0
        for i in self.queue:
            z = 0
            for j in item:
                z = z + 1
                if j == i:
                    theFirst = i
                    self.remove(theFirst)
                    if z == 0:
                        return 0
                    elif(z > 0):
                        return z-1
                    else:
                        return 0
