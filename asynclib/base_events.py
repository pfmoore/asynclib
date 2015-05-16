"""Event loop."""
from .tasks import Task

class EventLoop:
    def __init__(self):
        self.ready = []
        self.call_soon_queue = []
        self.running = False
    def call_soon(self, fn):
        self.call_soon_queue.append(fn)
    def _run_one_step(self):
        while self.call_soon_queue:
            fn = self.call_soon_queue.pop(0)
            fn()
        if not self.ready:
            return
        current = self.ready[0]
        try:
            next(current)
        except StopIteration:
            self.unschedule(current)
        else:
            if self.ready and self.ready[0] is current:
                # current is hogging the "next available" slot.
                # Implement a fairness algorithm here - in this case,
                # just move it to the back to give a "round robin"
                # algorithm
                del self.ready[0]
                self.ready.append(current)
    def run_forever(self):
        self.running = True
        while self.running and self.ready:
            self._run_one_step()
    def run_until_complete(future):
        pass
    def is_running(self):
        return self.running
    def stop(self):
        self.running = False
    def schedule(self, coro):
        self.ready.append(coro)
    def unschedule(self, coro):
        if coro in self.ready:
            self.ready.remove(coro)
    def create_task(self, coro):
        t = Task(coro, loop=self) # self.schedule(coro)
    def get_debug(self):
        return False
    def call_exception_handler(self, *args):
        print(args)

loop = EventLoop()
