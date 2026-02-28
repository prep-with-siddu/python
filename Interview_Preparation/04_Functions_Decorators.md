# 04 — Functions & Decorators — Interview Questions

> **40+ questions covering closures, decorators, generators, iterators, functools**

---

## 🔹 Section 1: Function Basics

### Q1. 🟢 What are the types of function arguments?

**Answer:**
```python
# 1. Positional arguments
def greet(name, age):
    print(f"{name}, {age}")
greet("Sid", 25)

# 2. Keyword arguments
greet(age=25, name="Sid")

# 3. Default arguments
def greet(name, age=25):
    print(f"{name}, {age}")
greet("Sid")  # age defaults to 25

# 4. *args — variable positional (tuple)
def total(*args):
    return sum(args)
total(1, 2, 3)  # 6

# 5. **kwargs — variable keyword (dict)
def info(**kwargs):
    print(kwargs)
info(name="Sid", age=25)  # {'name': 'Sid', 'age': 25}

# 6. Keyword-only (after *)
def func(a, b, *, c, d):
    pass
func(1, 2, c=3, d=4)  # c and d MUST be keyword

# 7. Positional-only (before /, Python 3.8+)
def func(a, b, /, c, d):
    pass
func(1, 2, c=3, d=4)  # a and b MUST be positional
```

**Full signature order:**
```python
def func(pos_only, /, normal, *, kw_only, **kwargs):
    pass
```

---

### Q2. 🟢 What is the difference between `return` and `yield`?

**Answer:**

| Feature | `return` | `yield` |
|---------|----------|---------|
| Terminates function | ✅ Yes | ❌ No (suspends) |
| Returns | Single value | Generator object |
| Memory | All at once | One at a time |
| State | Lost | Preserved |

```python
# return — all in memory
def get_squares_list(n):
    return [x**2 for x in range(n)]  # Entire list in memory

# yield — lazy, one at a time
def get_squares_gen(n):
    for x in range(n):
        yield x**2  # Generates one value, pauses

gen = get_squares_gen(1000000)
print(next(gen))  # 0
print(next(gen))  # 1
# Only 1 value in memory at a time!
```

---

### Q3. 🟡 What are first-class functions?

**Answer:**
In Python, functions are **first-class objects** — they can be:

```python
# 1. Assigned to variables
def greet():
    return "Hello"
say_hi = greet
print(say_hi())  # "Hello"

# 2. Passed as arguments
def apply(func, value):
    return func(value)
print(apply(len, "hello"))  # 5

# 3. Returned from functions
def multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = multiplier(2)
print(double(5))  # 10

# 4. Stored in data structures
funcs = [str.upper, str.lower, str.title]
for f in funcs:
    print(f("hello world"))
```

---

### Q4. 🟡 What is a lambda function? When to use it?

**Answer:**
Anonymous, single-expression function.

```python
# Lambda syntax
square = lambda x: x ** 2
add = lambda a, b: a + b

# Common uses:
# 1. sort key
users = [("Sid", 25), ("Raj", 30)]
users.sort(key=lambda u: u[1])

# 2. map/filter
nums = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, nums))
doubled = list(map(lambda x: x * 2, nums))

# 3. Quick callbacks
button.on_click(lambda: print("clicked"))
```

**Don't use when:**
- Logic is complex → use `def`
- Needs multiple statements → use `def`
- Reused in multiple places → use `def` with a name

---

## 🔹 Section 2: Closures

### Q5. 🟡 What is a closure?

**Answer:**
A closure is a function that remembers values from its enclosing scope, even after that scope finishes.

```python
def outer(message):
    # message is "enclosed" in the returned function
    def inner():
        print(message)  # Accesses message from outer
    return inner

greet = outer("Hello!")
greet()  # "Hello!" — remembers message even though outer() finished

# Check closure variables
print(greet.__closure__[0].cell_contents)  # "Hello!"
```

**3 requirements for a closure:**
1. Nested function
2. Inner function references variable from outer
3. Outer function returns inner function

---

### Q6. 🟡 Write a closure-based counter.

**Answer:**
```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c1 = make_counter()
print(c1())  # 1
print(c1())  # 2
print(c1())  # 3

c2 = make_counter()  # Independent counter
print(c2())  # 1
```

---

## 🔹 Section 3: Decorators

### Q7. 🟡 What is a decorator? How does it work?

**Answer:**
A decorator wraps a function to add behavior without modifying it.

```python
# A decorator is a function that takes a function and returns a function
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello {name}")

greet("Sid")
# Before
# Hello Sid
# After

# @ syntax is equivalent to:
# greet = my_decorator(greet)
```

---

### Q8. 🟡 Write a timing decorator.

**Answer:**
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()  # slow_function took 1.0012s
```

---

### Q9. 🟡 Why is `@wraps` important?

**Answer:**
Without `@wraps`, the decorated function loses its name, docstring, etc.

```python
from functools import wraps

def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def hello():
    """Says hello"""
    return "hi"

print(hello.__name__)  # "wrapper" ❌
print(hello.__doc__)   # None ❌

# Fix: Use @wraps
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def hello():
    """Says hello"""
    return "hi"

print(hello.__name__)  # "hello" ✅
print(hello.__doc__)   # "Says hello" ✅
```

---

### Q10. 🟡 Write a decorator with arguments.

**Answer:**
```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)    # repeat(3) returns the actual decorator
def greet(name):
    print(f"Hello {name}")

greet("Sid")
# Hello Sid
# Hello Sid
# Hello Sid
```

**3 levels:** 
- `repeat(3)` → returns `decorator`
- `decorator(greet)` → returns `wrapper`
- `wrapper("Sid")` → calls greet 3 times

---

### Q11. 🟡 Write a retry decorator.

**Answer:**
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    # Might fail due to network issues
    import requests
    return requests.get(url)
```

---

### Q12. 🟡 Write an authentication decorator (backend).

**Answer:**
```python
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return {"error": "Unauthorized"}, 401
        return func(request, *args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if role not in request.user.roles:
                return {"error": "Forbidden"}, 403
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

@require_auth
@require_role("admin")
def delete_user(request, user_id):
    # Only authenticated admins can reach here
    pass
```

---

### Q13. 🔴 Can you stack multiple decorators? What's the order?

**Answer:**
```python
def bold(func):
    def wrapper(): return f"<b>{func()}</b>"
    return wrapper

def italic(func):
    def wrapper(): return f"<i>{func()}</i>"
    return wrapper

@bold
@italic
def greet():
    return "Hello"

print(greet())  # <b><i>Hello</i></b>

# Equivalent to: greet = bold(italic(greet))
# Execution: bottom-up (italic first, then bold wraps it)
```

**Order:** Decorators are applied bottom-up, but executed top-down.

---

### Q14. 🔴 Write a class-based decorator.

**Answer:**
```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello {name}"

greet("Sid")  # greet called 1 times
greet("Raj")  # greet called 2 times
print(greet.count)  # 2
```

---

## 🔹 Section 4: Generators & Iterators

### Q15. 🟡 What is an iterator? What is the iterator protocol?

**Answer:**
An iterator implements two methods:
- `__iter__()` — returns self
- `__next__()` — returns next value or raises `StopIteration`

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for num in CountDown(5):
    print(num)  # 5, 4, 3, 2, 1
```

---

### Q16. 🟡 What is a generator? How is it different from an iterator?

**Answer:**
A generator is a simpler way to create iterators using `yield`.

```python
# Generator function (uses yield)
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# Generator expression (like list comp with parentheses)
squares = (x**2 for x in range(10))

for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

| Feature | Iterator (class) | Generator (function) |
|---------|-----------------|---------------------|
| Implementation | `__iter__` + `__next__` | `yield` keyword |
| Code | More boilerplate | Less code |
| State | Manual | Automatic |
| Memory | Depends | Always lazy |

---

### Q17. 🟡 What is `yield from`?

**Answer:**
Delegates to a sub-generator.

```python
# Without yield from
def flatten(nested):
    for sublist in nested:
        for item in sublist:
            yield item

# With yield from — cleaner
def flatten(nested):
    for sublist in nested:
        yield from sublist

list(flatten([[1, 2], [3, 4], [5, 6]]))
# [1, 2, 3, 4, 5, 6]

# Chaining generators
def gen1():
    yield from range(3)    # 0, 1, 2
    yield from range(10, 13)  # 10, 11, 12

list(gen1())  # [0, 1, 2, 10, 11, 12]
```

---

### Q18. 🟡 Write a generator for reading a large file line by line.

**Answer:**
```python
def read_large_file(file_path):
    """Memory-efficient file reading"""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# Process millions of lines with constant memory
for line in read_large_file("huge_log.txt"):
    if "ERROR" in line:
        print(line)

# Count lines without loading full file
error_count = sum(1 for line in read_large_file("huge_log.txt") if "ERROR" in line)
```

---

### Q19. 🔴 What is `send()` in generators?

**Answer:**
`send()` sends a value INTO a running generator.

```python
def accumulator():
    total = 0
    while True:
        value = yield total  # yield sends total OUT, receives value IN
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)        # Initialize (must call next first) → 0
gen.send(10)     # → 10
gen.send(20)     # → 30
gen.send(5)      # → 35
```

**Backend use:** Coroutines, async patterns, data pipelines.

---

## 🔹 Section 5: functools Module

### Q20. 🟡 What is `functools.lru_cache`?

**Answer:**
LRU (Least Recently Used) cache — memoizes function results.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(100)  # Instant! (without cache: impossibly slow)

# Check cache stats
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)

# Clear cache
fibonacci.cache_clear()
```

**Important:** Arguments must be hashable (no lists/dicts).

---

### Q21. 🟡 What is `functools.partial`?

**Answer:**
Creates a new function with some arguments pre-filled.

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(3))    # 27

# Backend use: Pre-configured functions
import requests
json_get = partial(requests.get, headers={"Accept": "application/json"})
json_get("https://api.example.com/data")
```

---

### Q22. 🟡 What is `functools.reduce`?

**Answer:**
Applies a function cumulatively to items, reducing to a single value.

```python
from functools import reduce

# Sum
nums = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, nums)  # 15

# How it works:
# Step 1: 1 + 2 = 3
# Step 2: 3 + 3 = 6
# Step 3: 6 + 4 = 10
# Step 4: 10 + 5 = 15

# Max value
max_val = reduce(lambda a, b: a if a > b else b, nums)  # 5

# Flatten list
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda a, b: a + b, nested)  # [1, 2, 3, 4, 5, 6]
```

---

### Q23. 🟡 What are `map()`, `filter()`, and `reduce()`?

**Answer:**
```python
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map — transform each element
squares = list(map(lambda x: x**2, nums))
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# filter — keep elements that match condition
evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4, 6, 8, 10]

# reduce — combine into single value
from functools import reduce
total = reduce(lambda a, b: a + b, nums)
# 55
```

**Pythonic alternatives (preferred):**
```python
# List comprehension instead of map + filter
squares = [x**2 for x in nums]
evens = [x for x in nums if x % 2 == 0]

# sum() instead of reduce for addition
total = sum(nums)
```

---

## 🔹 Section 6: Context Managers

### Q24. 🟡 What is a context manager? How to create one?

**Answer:**
Context managers handle setup and cleanup with `with` statement.

```python
# Method 1: Class-based (__enter__ / __exit__)
class DBConnection:
    def __enter__(self):
        self.conn = create_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return False  # Don't suppress exceptions

with DBConnection() as conn:
    conn.execute("SELECT 1")  # auto-closes after block

# Method 2: Generator-based (simpler)
from contextlib import contextmanager

@contextmanager
def db_connection():
    conn = create_connection()
    try:
        yield conn      # Everything before yield = __enter__
    finally:
        conn.close()    # Everything after yield = __exit__

with db_connection() as conn:
    conn.execute("SELECT 1")
```

---

### Q25. 🟡 What is `contextlib.suppress`?

**Answer:**
```python
from contextlib import suppress

# Instead of:
try:
    os.remove("temp.txt")
except FileNotFoundError:
    pass

# Use:
with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

---

## 🔹 Section 7: Tricky Questions

### Q26. 🟡 What is the output?

```python
funcs = []
for i in range(5):
    funcs.append(lambda: i)

print([f() for f in funcs])
```

**Answer:** `[4, 4, 4, 4, 4]`

All lambdas capture the **same** variable `i`, which ends at 4.

**Fix:**
```python
funcs = []
for i in range(5):
    funcs.append(lambda i=i: i)  # Default arg captures current i

print([f() for f in funcs])  # [0, 1, 2, 3, 4]
```

---

### Q27. 🟡 What is the output?

```python
def make_functions():
    return [lambda x: x * i for i in range(5)]

funcs = make_functions()
print(funcs[0](10))
print(funcs[3](10))
```

**Answer:** `40` and `40` — Same closure trap. `i` is 4 for all.

---

### Q28. 🟡 What is the output?

```python
def func(a, b=[]):
    b.append(a)
    return b

print(func(1))
print(func(2))
print(func(3, []))
print(func(4))
```

**Answer:**
```
[1]
[1, 2]
[3]          # New list passed
[1, 2, 4]   # Back to the default shared list!
```

---

### Q29. 🟡 What is a higher-order function?

**Answer:**
A function that takes a function as argument OR returns a function.

```python
# Takes function as argument
def apply_twice(func, value):
    return func(func(value))

print(apply_twice(lambda x: x + 3, 7))  # 13

# Returns a function
def create_adder(n):
    return lambda x: x + n

add5 = create_adder(5)
print(add5(10))  # 15
```

**Examples in Python:** `map()`, `filter()`, `sorted(key=)`, `@decorator`

---

### Q30. 🟡 What is `*` (unpacking) in function calls?

**Answer:**
```python
# * unpacks iterables
def func(a, b, c):
    print(a, b, c)

args = [1, 2, 3]
func(*args)  # 1 2 3

# ** unpacks dicts
kwargs = {"a": 1, "b": 2, "c": 3}
func(**kwargs)  # 1 2 3

# Collecting remaining
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5
```

---

## 🔹 Section 8: Backend-Specific Function Patterns

### Q31. 🟡 Write a rate limiter using a decorator.

**Answer:**
```python
import time
from functools import wraps

def rate_limit(max_calls, period):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            while calls and calls[0] < now - period:
                calls.pop(0)
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=5, period=60)  # 5 calls per minute
def api_call():
    return "success"
```

---

### Q32. 🟡 Write a caching decorator with TTL.

**Answer:**
```python
import time
from functools import wraps

def cache_with_ttl(ttl=300):  # 5 minutes default
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl:
                    return result  # Cache hit
            
            result = func(*args)
            cache[args] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

@cache_with_ttl(ttl=60)
def get_user(user_id):
    # Expensive database call
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

---

### Q33. 🟡 What is `functools.singledispatch`?

**Answer:**
Overloads function based on the type of first argument.

```python
from functools import singledispatch

@singledispatch
def process(data):
    raise TypeError(f"Unsupported: {type(data)}")

@process.register(str)
def _(data):
    return f"String: {data.upper()}"

@process.register(int)
def _(data):
    return f"Int: {data * 2}"

@process.register(list)
def _(data):
    return f"List: {len(data)} items"

print(process("hello"))  # String: HELLO
print(process(5))         # Int: 10
print(process([1, 2]))    # List: 2 items
```

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | What is a closure? | Function that remembers enclosing scope |
| 2 | What does a decorator do? | Wraps function to add behavior |
| 3 | Why use `@wraps`? | Preserves original function metadata |
| 4 | `*args` vs `**kwargs`? | Positional tuple vs keyword dict |
| 5 | Generator vs list? | Lazy (one-at-a-time) vs all-in-memory |
| 6 | What does `yield` do? | Produces value, suspends function |
| 7 | What is `lru_cache`? | Memoization decorator |
| 8 | Lambda limitation? | Single expression only |
| 9 | Context manager protocol? | `__enter__` + `__exit__` |
| 10 | Higher-order function? | Takes or returns a function |

---

*Next: [05_Error_Handling_Files.md](05_Error_Handling_Files.md)*
