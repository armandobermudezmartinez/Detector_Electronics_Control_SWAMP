import sched
import time

# Intializing s as the scheduler object
s = sched.scheduler(time.time, time.sleep)

# Creating a method to print time


def print_time(a="default"):
    print("From print_time", time.time(), a)

# Method to print a few times pre-decided


def print_some_times():
    print("This is the current time : ", time.time())

    # default command to print time
    s.enter(10, 1, print_time)

    # passing an argument to be printed after the time
    s.enter(10, 1, print_time, argument=('positional',))

    # passing a keyword argument to print after the time
    s.enter(10, 1, print_time, kwargs={'a': 'keyword'})

    # runs the scheduler object
    s.run()
    print("Time at which the program comes to an end: ", time.time())

# Output
# This is the current time :  1609002547.484134
# From print_time 1609002557.4923606 default
# From print_time 1609002557.4923606 positional
# From print_time 1609002557.4923606 keyword
# Time at which the program comes to an end :  1609002557.4923606
