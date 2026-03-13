""" This file is just for practice for the write the decorator function 
"""
"""
Decorator Function Documentation
==================================
WHAT IS A DECORATOR?
A decorator is a function that takes another function as an argument and returns a new function.
It allows you to "wrap" a function with additional functionality without modifying the original function.
HOW DOES THE write_decorator() WORK?
=====================================
Flow of Execution:
1. @write_decorator is applied to my_function()
2. Python calls: my_function = write_decorator(my_function)
3. The original my_function is passed as 'func' parameter to write_decorator()
4. write_decorator() returns the wrapper function
5. When you call my_function(), you're actually calling wrapper()
6. wrapper() executes the original function using func(*args, **kwargs)
7. Results are returned to the caller
Step-by-Step Flow:
    # Is equivalent to:
    my_function = write_decorator(my_function)
    # When called:
    my_function()  # Calls wrapper()
                   # which calls the original func()
                   # and returns its result
PARAMETERS EXPLAINED:
- *args: Captures positional arguments passed to the decorated function
- **kwargs: Captures keyword arguments passed to the decorated function
QUESTIONS FOR PRACTICE:
=======================
1. What is the purpose of *args and **kwargs in a decorator?
2. How would you modify write_decorator() to log when a function starts and ends execution?
3. Create a decorator that measures the execution time of a function.
4. Write a decorator that retries a function up to 3 times if it raises an exception.
5. How would you create a decorator that caches the results of a function (memoization)?
6. Create a decorator that validates if the input arguments meet certain conditions before executing the function.
7. Write a decorator that converts the return value of a function to uppercase (if it's a string).
TRY THESE ADVANCED CHALLENGES:
==============================
- Create a decorator that accepts parameters itself (decorator with arguments)
- Create a decorator that works with class methods
- Create a decorator that preserves the original function's metadata using functools.wraps """
"""
bascically decorator means is a function that takes another function as 
an argument and returns a new function """
""" Decorators are widely used in Python for various practical applications: 
Bhrighu Academy
Bhrighu Academy
Logging: To track function calls, arguments, and return values for debugging or monitoring without cluttering the business logic.
Authentication/Authorization: To verify user permissions or API keys before allowing a function to execute, common in web frameworks like Flask and Django.
Timing/Performance Monitoring: To measure the execution time of a function to identify performance bottlenecks.
Caching/Memoization: To store the results of expensive function calls and return the cached result for repeated inputs, often using functools.lru_cache.
Error Handling/Retry Logic: To wrap functions with try-except blocks or automatically retry failed operations (e.g., network calls) to add resilience. 

"""


"""
Python provides several powerful built-in decorators, especially for use within classes: 
GeeksforGeeks
GeeksforGeeks
 +1
@staticmethod: Defines a method that doesn't receive self or cls as an implicit first argument,
behaving like a normal function but belonging to the class's namespace.
@classmethod: Defines a method that receives the class (cls) as its first 
argument, allowing it to access and modify class-level state.
@property: Allows a method to be accessed as an attribute, which is 
useful for implementing getters and setters for class attributes in an 
encapsulated way.
@functools.wraps: A decorator used within custom decorators to preserve 
the original function's name, docstring, and other metadata, which helps 
with introspection and debugging.

"""
def write_decorator(func):
    def wrapper(*args, **kwargs):
        # Perform write operation before calling the original function
        result = func(*args, **kwargs)
        results  = result * 3
        # Perform write operation after calling the original function
        return results
    return wrapper


@write_decorator
def my_function():
    output = 1 + 1 *34

    return output



print(my_function())



import functools

def log_function_call(func):
    """A decorator that logs a function call."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

@log_function_call
def add(a, b):
    return a + b

# Calling the decorated function
add(3, 5)


