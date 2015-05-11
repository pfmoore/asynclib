def coroutine(f):
    """Marks a coroutine. No-op in this implementation."""
    return f

class EventLoop:
    def __init__(self):
        self.ready = []
        self.running = False
        self.current = None
    def run_forever(self):
        self.running = True
        # This does *not* run forever, but instead just runs
        # until the ready queue is empty...
        while self.running:
            self._run_one_step()
    def run_until_complete(self, coro):
        # yield from coro -> runs coro until complete...
        result = None
        def runner():
            nonlocal result
            result = yield from coro
            self.stop()
            yield
        self.schedule(runner)
        self.run_forever()
        return result
    def is_running(self):
        return self.running
    def stop(self):
        self.running = False
    # Not needed?
    def is_closed(self):
        pass
    def close(self):
        pass
    # Internal methods
    def schedule(self, coro):
        self.ready.append(coro)
    def unschedule(self, coro=None):
        if coro is None:
            coro = self.current
        if coro in self.ready:
            self.ready.remove(coro)
        return coro
    # Optional methods
    def create_task(self, coro):
        self.schedule(coro)
    def call_soon(self, function):
        pass
    # call_soon_threadsafe? Generally, consider thread safety...
    # Error handling API
    # Debug mode
    # Implementation details
    def _run_one_step(self):
        if not self.ready:
            return
        self.current = self.ready[0]
        try:
            print(self.current)
            next(self.current)
        except StopIteration:
            self.unschedule(self.current)
        else:
            if self.ready and self.ready[0] is self.current:
                # current is hogging the "next available" slot.
                # Implement a fairness algorithm here - in this case,
                # just move it to the back to give a "round robin"
                # algorithm
                del self.ready[0]
                self.ready.append(self.current)
        self.current = None

class Lock:
    def __init__(self, *, loop=None):
        pass
    def locked(self):
        pass
    @coroutine
    def acquire(self):
        pass
    def release(self):
        pass

class Event:
    def __init__(self, *, loop=None):
        self.state = False
    def clear(self):
        self.state = False
    def is_set(self):
        return self.state
    def set(self):
        self.state = True
    @coroutine
    def wait(self):
        # Busy wait - a bit of a hack for now
        while True:
            if self.state:
                return
            yield

class Condition:
    def __init__(self, lock=None, *, loop=None):
        pass
    @coroutine
    def acquire(self):
        pass
    def notify(self, n=1):
        pass
    def locked(self):
        pass
    def notify_all(self):
        pass
    def release(self):
        pass
    @coroutine
    def wait(self):
        pass
    @coroutine
    def wait_for(self, predicate):
        pass

class Semaphore:
    id = 0
    def __init__(self, value=1, *, loop=None):
        self.value = value
        self.queue = []
        self.loop = loop
        Semaphore.id += 1
        self.id = Semaphore.id
    def __repr__(self):
        return "<Semaphore{} value={}>".format(self.id, self.value)
    @coroutine
    def acquire(self):
        if self.locked():
            self.queue.append(self.loop.unschedule())
            yield
        self.value -= 1
    def locked(self):
        return self.value == 0
    def release(self):
        self.value += 1
        if self.queue:
            self.loop.schedule(self.queue.pop(0))

class BoundedSemaphore(Semaphore):
    def __init__(self, value=1, *, loop=None):
        pass
    @coroutine
    def acquire(self):
        pass
    def locked(self):
        pass
    def release(self):
        pass

class Queue:
    def __init__(self, maxsize=0, *, loop=None):
        self.maxsize = maxsize
    def empty(self):
        pass
    def full(self):
        pass
    @coroutine
    def get(self):
        pass
    def get_nowait(self):
        pass
    @coroutine
    def join(self):
        pass
    @coroutine
    def put(self, item):
        pass
    def put_nowait(self, item):
        pass
    def qsize(self):
        pass
    def task_done(self):
        pass

class PriorityQueue(Queue):
    pass

class LifoQueue(Queue):
    pass

class QueueEmpty(Exception):
    pass

class QueueFull(Exception):
    pass
