from asynclib import base_events, events
from asynclib import locks
from asynclib.coroutines import coroutine

@coroutine
def philosopher(name, lifetime, think_time, eat_time, left_fork, right_fork):
    for i in range(lifetime):
        for j in range(think_time):
            print(name, "thinking")
            yield
        print(name, "waiting for fork", left_fork)
        yield from left_fork.acquire()
        print(name, "acquired fork", left_fork)
        print(name, "waiting for fork", right_fork)
        yield from right_fork.acquire()
        print(name, "acquired fork", right_fork)
        for j in range(eat_time):
            # They're Python philosophers, so they eat spam rather than spaghetti
            print(name, "eating spam")
            yield
        print(name, "releasing forks", left_fork, "and", right_fork)
        left_fork.release()
        right_fork.release()
    print(name, "leaving the table")

loop = base_events.loop

forks = [locks.Semaphore(i, loop=loop) for i in range(3)]
loop.create_task(philosopher("Plato", 7, 2, 3, forks[0], forks[1]))
loop.create_task(philosopher("Socrates", 8, 3, 1, forks[1], forks[2]))
loop.create_task(philosopher("Euclid", 5, 1, 4, forks[2], forks[0]))
loop.run_forever()
