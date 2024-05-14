# Importing the time function from the time module to measure execution time
from time import time

mem = {}                                               # Define a global dictionary to store timing information for functions

# Define a decorator function to measure the execution time of other functions
def time_fn(func):

    # Define the inner function that wraps the original function
    def measure_time(*arg, **kwarg):

        func_name = func.__name__                      # Get the name of the function being decorated

        # If this is the first time the function is called, initialize its entry in mem
        if func_name not in mem.keys():
            mem[func_name] = {
                "n": 0,                                 # Counter for the number of times the function has been called
                "time": 0                               # Accumulator for the total execution time of the function
            }
        start = time()                                  # Record the start time before calling the function
        func(*arg, **kwarg)                             # Call the original function with the provided arguments and keyword arguments
        mem[func_name]["n"] += 1                        # Increment the call counter

        mem[func_name]["time"] += time() - start        # Add the elapsed time to the total execution time
        if mem[func_name]["n"] == 60:                   # If the function has been called 60 times, print the average execution time
            print("execution time of the function "+ func_name + " - " + str(mem[func_name]["time"]))
            mem[func_name]["n"] = 0                     # Reset the call counter and total execution time for the function
            mem[func_name]["time"] = 0
    return measure_time                                 # Return the inner function to be used as the decorated function
