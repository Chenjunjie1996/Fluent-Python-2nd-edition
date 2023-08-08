"""
How Python evaluates decorator syntax
How python decides whether a variable is local
Why closures exist and how they work
What problem is solved by nonlocal
Implementing a well-behaved decorator
Powerful decorators in the standard library: @cache, @lru_cache, @singledispatch
Implementing a parameterized decorator
"""
import functools
import time

# Decorators 101
"""
@decorate
def target():
    print("running target()")

def target():
    print("running target()")
target = decorate(target)
"""

def deco(func):
    def inner():
        print("running inner()")
    return inner

@deco
def target():
    print("running target()")

target()

"""
deco returns its inner function object.
target is decorated by deco.
Invoking the decorated target actually runs inner.
Inspection reveals that target is a now a reference to inner.
"""

"""
Three essential facts make a good summary of decorators:
• A decorator is a function or another callable.
• A decorator may replace the decorated function with a different one.
• Decorators are executed immediately when a module is loaded.
"""

# When Python Executes Decorators
registry = []
def register(func):
    print(f"running register({func})")
    registry.append(func)
    return func

@register
def f1():
    print("running f1()")

@register
def f2():
    print("running f2()")

def f3():
    print("running f3()")

f1()
f2()
f3()
print(registry)

# Registration Decorators
"""
• The decorator function is defined in the same module as the decorated functions.
A real decorator is usually defined in one module and applied to functions in
other modules.
• The register decorator returns the same function passed as an argument. In
practice, most decorators define an inner function and return it.

Most decorators do change the decorated function. They usually do it by defining an
inner function and returning it to replace the decorated function. Code that uses
inner functions almost always depends on closures to operate correctly. To under‐
stand closures, we need to take a step back and review how variable scopes work in
Python.
"""

# Variable Scope Rules
b = 6
def f3(a):
    global b
    print(a)
    print(b)
    b = 9
f3(3)

# Closures
def make_averager():
    series = []

    def averager(new_value):
        # series is free variable
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager

avg = make_averager()
print(avg(10))
print(avg(11))
print(avg(15))

print(avg.__code__.co_varnames)
print(avg.__code__.co_freevars)
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
"""
如果一个变量在函数代码块中定义，但在其他代码块中被使用，例如嵌套在外部函数中的闭包函数，那么它就是自由变量
series在make_averager()中是局部变量，在averager()中是自由变量，因为它在averager()中没有绑定

The value for series is kept in the __closure__ attribute of the returned function
avg. Each item in avg.__closure__ corresponds to a name in 
avg. __code__.co_freevars. These items are cells, and they have an attribute called 
cell_contents where the actual value can be found. Example 9-11 shows these attributes.

Summarize:
a closure is a function that retains the bindings of the free variables
that exist when the function is defined, so that they can be used later when the func‐
tion is invoked and the defining scope is no longer available.
Note that the only situation in which a function may need to deal with external vari‐
ables that are nonglobal is when it is nested in another function and those variables
are part of the local scope of the outer function.
"""

# The nonlocal Declaration
def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return averager

# Variable Lookup Logic
"""
• If there is a global x declaration, x comes from and is assigned to the x global
variable module.4
• If there is a nonlocal x declaration, x comes from and is assigned to the x local
variable of the nearest surrounding function where x is defined.
• If x is a parameter or is assigned a value in the function body, then x is the local
variable.
• If x is referenced but is not assigned and is not a parameter:
— x will be looked up in the local scopes of the surrounding(nonlocal scopes).
— If not found in surrounding scopes, it will be read from the module global scope.
— If not found in the global scope, it will be read from __builtins__.__dict__.
"""

# Implementing a Simple Decorator
"""
This is the typical behavior of a decorator: it replaces the decorated function with a
new function that accepts the same arguments and (usually) returns whatever the
decorated function was supposed to return, while also doing some extra processing.
"""
def clock(func):
    """
    1. Records the initial time t0
    2. Calls the original factorial function, saving the result
    3. Computes the elapsed time
    4. Formats and displays the collected data
    5. Returns the result saved in step2
    """
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

snooze(.123)
print("6! =" ,factorial(6))

# How It Works

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

# same as:
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)
factorial = clock(factorial)

print(factorial.__name__)

def clock(func):
    """an improved clock decorator
    1. support keyword arguments
    2. it masks the __name__ and __doc__ of the decorated function
    """
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
        arg_str = ', '.join(arg_lst)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked

# Decorators in the Standard Library:
# Memoization with functools.cache
@functools.cache
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)
print(fibonacci(6))

# Using lru_cache In long-running processes
"""
Set the maximum number of entries to be stored.

Determines whether the results of different argument types 
are stored separately. eg f(1) f(1.0)
If typed=True, those arguments would produce different entries
"""
@functools.lru_cache(maxsize=2**20, typed=True)
def costly_function(a, b):
    pass

# Single Dispatch Generic Functions
