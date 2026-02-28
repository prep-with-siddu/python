# 06 — Advanced Python — Interview Questions

> **50+ questions covering concurrency, async, metaclasses, descriptors, GIL deep dive**

---

## 🔹 Section 1: Concurrency & Parallelism

### Q1. 🟡 What is the difference between concurrency and parallelism?

**Answer:**

| | Concurrency | Parallelism |
|-|-------------|-------------|
| Definition | Multiple tasks in progress | Multiple tasks running simultaneously |
| CPU cores | Single core possible | Requires multiple cores |
| Python | `threading`, `asyncio` | `multiprocessing` |
| Analogy | One cook, multiple dishes | Multiple cooks |

```
Concurrency:  Task A ──▶ pause ──▶ Task A
              Task B ──▶ pause ──▶ Task B
              (interleaved on one core)

Parallelism:  Core 1: Task A ────────────▶
              Core 2: Task B ────────────▶
              (truly simultaneous)
```

---

### Q2. 🟡 Threading vs Multiprocessing vs Asyncio — when to use each?

**Answer:**

| | Threading | Multiprocessing | Asyncio |
|-|-----------|----------------|---------|
| Best for | I/O-bound | CPU-bound | I/O-bound (many connections) |
| GIL | Limited by GIL | Bypasses GIL | Not affected |
| Memory | Shared | Separate per process | Shared |
| Overhead | Low | High (process creation) | Very low |
| Typical use | File I/O, DB queries | Data processing, ML | Web servers, APIs |

```python
# Threading — I/O-bound (network calls)
import threading
threads = [threading.Thread(target=fetch, args=(url,)) for url in urls]

# Multiprocessing — CPU-bound (computation)
from multiprocessing import Pool
with Pool(4) as pool:
    results = pool.map(heavy_compute, data)

# Asyncio — I/O-bound (many concurrent connections)
import asyncio
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)
```

---

### Q3. 🔴 Explain the GIL in detail. How does it affect threading?

**Answer:**
The **Global Interpreter Lock (GIL)** is a mutex in CPython that allows only ONE thread to execute Python bytecode at a time.

```
Thread 1: acquire GIL → execute → release GIL → wait
Thread 2: wait → acquire GIL → execute → release GIL
Thread 3: wait → wait → acquire GIL → execute
```

**Why it exists:**
- CPython's memory management uses reference counting
- Reference counting is NOT thread-safe
- GIL makes single-threaded code faster
- Simplifies C extension development

**Impact on threading:**
```python
# ❌ CPU-bound — GIL kills performance
import threading

def count(n):
    while n > 0:
        n -= 1

# Single thread: ~4 seconds
count(100_000_000)

# Two threads: ~8 seconds (SLOWER due to GIL contention!)
t1 = threading.Thread(target=count, args=(50_000_000,))
t2 = threading.Thread(target=count, args=(50_000_000,))

# ✅ I/O-bound — GIL is released during I/O
import requests
# Threads work great here — GIL released during network wait
```

**GIL is released during:**
- File I/O operations
- Network operations
- `time.sleep()`
- C extensions (e.g., NumPy operations)

---

### Q4. 🟡 Explain `concurrent.futures`. ThreadPoolExecutor vs ProcessPoolExecutor.

**Answer:**
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def fetch_url(url):
    time.sleep(1)  # Simulate I/O
    return f"Fetched {url}"

def compute(n):
    return sum(i * i for i in range(n))

# ThreadPoolExecutor — I/O-bound tasks
with ThreadPoolExecutor(max_workers=5) as executor:
    urls = ["url1", "url2", "url3"]
    futures = [executor.submit(fetch_url, url) for url in urls]
    for future in futures:
        print(future.result())

# ProcessPoolExecutor — CPU-bound tasks
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, [10**6, 10**6, 10**6]))

# as_completed — get results as they finish
from concurrent.futures import as_completed
with ThreadPoolExecutor(5) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        print(f"{url}: {future.result()}")
```

---

### Q5. 🔴 What is `asyncio`? Explain `async/await`.

**Answer:**
`asyncio` is Python's built-in asynchronous I/O framework — single-threaded concurrency.

```python
import asyncio

async def fetch_data(name, delay):
    print(f"Starting {name}")
    await asyncio.sleep(delay)    # Non-blocking wait
    print(f"Finished {name}")
    return f"{name} result"

async def main():
    # Sequential — 3 seconds total
    r1 = await fetch_data("A", 1)
    r2 = await fetch_data("B", 2)
    
    # Concurrent — 2 seconds total (max of delays)
    results = await asyncio.gather(
        fetch_data("A", 1),
        fetch_data("B", 2),
        fetch_data("C", 1),
    )
    print(results)

asyncio.run(main())
```

**Key concepts:**
| Term | Meaning |
|------|---------|
| `async def` | Defines a coroutine |
| `await` | Suspends until result ready |
| `asyncio.gather()` | Run multiple coroutines concurrently |
| `asyncio.create_task()` | Schedule coroutine |
| Event loop | Manages all async operations |

---

### Q6. 🔴 What is the difference between `asyncio.gather()` and `asyncio.wait()`?

**Answer:**
```python
import asyncio

async def task(n):
    await asyncio.sleep(n)
    return n

# gather — returns results in order
results = await asyncio.gather(task(2), task(1), task(3))
# [2, 1, 3] — same order as input

# wait — returns sets of done/pending
done, pending = await asyncio.wait(
    [task(2), task(1), task(3)],
    return_when=asyncio.FIRST_COMPLETED  # or ALL_COMPLETED
)
for t in done:
    print(t.result())
```

| Feature | `gather` | `wait` |
|---------|----------|--------|
| Returns | Ordered results | Sets of tasks |
| Error handling | Raises first error | All tasks complete |
| Cancellation | Cancel all on error | Flexible |
| Use case | Simple parallel | Fine-grained control |

---

### Q7. 🟡 What are thread-safe data structures in Python?

**Answer:**
```python
import queue
import threading

# Thread-safe queue
q = queue.Queue()
q.put(item)
item = q.get()

# Thread-safe with Lock
lock = threading.Lock()
shared_data = []

def thread_safe_append(item):
    with lock:
        shared_data.append(item)

# Thread-safe counter
counter = threading.local()  # Thread-local storage

# Built-in atomic operations (due to GIL)
# list.append(), dict[key]=value — atomic in CPython
# BUT: Don't rely on this! Use locks for safety.
```

---

## 🔹 Section 2: Iterators & Generators (Advanced)

### Q8. 🟡 What is the iterator protocol?

**Answer:**
```python
class InfiniteCounter:
    def __init__(self, start=0):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = self.current
        self.current += 1
        return value

# Usage
counter = InfiniteCounter(10)
print(next(counter))  # 10
print(next(counter))  # 11

# With for loop (need a break!)
for num in InfiniteCounter():
    if num > 5:
        break
    print(num)
```

---

### Q9. 🔴 What is a coroutine? How is it different from a generator?

**Answer:**
```python
# Generator — produces values (yield OUT)
def producer():
    for i in range(5):
        yield i

# Coroutine (old style) — consumes values (send IN + yield OUT)
def averager():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = averager()
next(avg)          # Prime the coroutine
avg.send(10)       # 10.0
avg.send(20)       # 15.0
avg.send(30)       # 20.0

# Modern coroutine (async/await)
async def fetch():
    data = await get_from_db()
    return data
```

---

### Q10. 🟡 What are `itertools` functions every backend dev should know?

**Answer:**
```python
from itertools import (
    chain, islice, groupby, zip_longest,
    product, combinations, permutations,
    accumulate, repeat, cycle, count,
    filterfalse, takewhile, dropwhile
)

# chain — flatten iterables
list(chain([1, 2], [3, 4]))  # [1, 2, 3, 4]

# islice — slice any iterable
list(islice(range(100), 5, 10))  # [5, 6, 7, 8, 9]

# groupby — group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))

# product — cartesian product
list(product("AB", "12"))  # [('A','1'), ('A','2'), ('B','1'), ('B','2')]

# combinations / permutations
list(combinations("ABC", 2))   # [('A','B'), ('A','C'), ('B','C')]
list(permutations("ABC", 2))   # [('A','B'), ('A','C'), ('B','A'), ...]

# accumulate — running total
list(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10]

# batch (Python 3.12+)
# list(itertools.batched(range(10), 3))  # [[0,1,2], [3,4,5], [6,7,8], [9]]
```

---

## 🔹 Section 3: Metaclasses & Descriptors

### Q11. 🔴 What are metaclasses?

**Answer:**
A metaclass is the class of a class. `type` is the default metaclass.

```python
# Everything is an object, classes are objects too
class Foo:
    pass

print(type(Foo))        # <class 'type'>
print(type(type))       # <class 'type'>

# Creating class dynamically with type()
MyClass = type('MyClass', (object,), {'x': 5, 'greet': lambda self: "hi"})
obj = MyClass()
print(obj.x)      # 5
print(obj.greet()) # "hi"

# Custom metaclass
class ValidateMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Enforce all methods have docstrings
        for key, value in namespace.items():
            if callable(value) and not key.startswith('_'):
                if not value.__doc__:
                    raise TypeError(f"{name}.{key}() must have a docstring")
        return super().__new__(mcs, name, bases, namespace)

class API(metaclass=ValidateMeta):
    def get_users(self):
        """Returns all users"""  # Required!
        pass
```

---

### Q12. 🔴 What are descriptors?

**Answer:**
Objects that customize attribute access via `__get__`, `__set__`, `__delete__`.

```python
class TypeChecked:
    def __init__(self, expected_type):
        self.expected_type = expected_type
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")
        setattr(obj, self.private_name, value)

class User:
    name = TypeChecked(str)
    age = TypeChecked(int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("Sid", 25)    # ✅
# User("Sid", "25")    # TypeError: age must be int
```

**Data vs Non-data descriptor:**
| Type | Has | Priority |
|------|-----|----------|
| Data descriptor | `__get__` + `__set__` | Higher than instance `__dict__` |
| Non-data descriptor | Only `__get__` | Lower than instance `__dict__` |

---

## 🔹 Section 4: Memory & Performance

### Q13. 🟡 How does Python memory allocation work?

**Answer:**
```
                Python Memory Architecture
┌────────────────────────────────────────────┐
│            Python Objects (heap)            │
├────────────────────────────────────────────┤
│   Object-Specific Allocators               │
│   (int, float, list, dict, etc.)          │
├────────────────────────────────────────────┤
│   PyMalloc (for objects < 512 bytes)       │
│   - Arena → Pool → Block                  │
│   - 256KB arenas, 4KB pools               │
├────────────────────────────────────────────┤
│   C malloc / OS memory                     │
└────────────────────────────────────────────┘
```

**Small object allocator (PyMalloc):**
- For objects < 512 bytes
- Pre-allocates pools of fixed-size blocks
- 8-byte aligned blocks (8, 16, 24, ... 512)
- Reduces `malloc()` calls

---

### Q14. 🟡 What are weak references?

**Answer:**
References that don't increase reference count — object can be garbage collected.

```python
import weakref

class Cache:
    def __init__(self, data):
        self.data = data

obj = Cache("important data")
weak = weakref.ref(obj)

print(weak())        # <Cache object> — still alive
print(weak().data)   # "important data"

del obj              # Object freed (ref count = 0)
print(weak())        # None — object was collected

# WeakValueDictionary — values are weak references
cache = weakref.WeakValueDictionary()
obj = Cache("data")
cache["key"] = obj
print(cache["key"])  # Works
del obj
# cache["key"]       # KeyError — auto removed
```

**Backend use:** Caching, observer pattern, preventing memory leaks.

---

### Q15. 🟡 What is `__slots__` and how does it save memory?

**Answer:**
```python
import sys

class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

a = WithDict(1, 2)
b = WithSlots(1, 2)

print(sys.getsizeof(a) + sys.getsizeof(a.__dict__))  # ~152 bytes
print(sys.getsizeof(b))                                # ~56 bytes

# ~63% less memory!
# Also: 10-15% faster attribute access
```

---

### Q16. 🟡 How to profile Python code?

**Answer:**
```python
# 1. time module — simple timing
import time
start = time.perf_counter()
# ... code ...
print(f"Took {time.perf_counter() - start:.4f}s")

# 2. timeit — accurate microbenchmarking
import timeit
timeit.timeit('sum(range(1000))', number=10000)

# 3. cProfile — function-level profiling
import cProfile
cProfile.run('my_function()')

# 4. memory_profiler — line-by-line memory
# pip install memory_profiler
# @profile
# def func(): ...
# python -m memory_profiler script.py

# 5. line_profiler — line-by-line time
# pip install line_profiler
# @profile
# def func(): ...
# kernprof -l script.py
```

---

## 🔹 Section 5: Type Hints & Static Analysis

### Q17. 🟡 What are type hints? Why use them?

**Answer:**
```python
# Basic type hints (PEP 484)
def greet(name: str) -> str:
    return f"Hello {name}"

# Complex types
from typing import List, Dict, Optional, Union, Tuple

def get_users() -> List[Dict[str, str]]:
    return [{"name": "Sid"}]

def find_user(user_id: int) -> Optional[dict]:
    return None  # or user dict

def process(data: Union[str, bytes]) -> str:
    return str(data)

# Python 3.10+ — cleaner syntax
def process(data: str | bytes) -> str:
    return str(data)

def find_user(user_id: int) -> dict | None:
    return None
```

**Why type hints for backend:**
- Self-documenting API contracts
- IDE autocomplete and error detection
- `mypy` catches bugs before runtime
- Required by FastAPI / Pydantic

---

### Q18. 🟡 What is `TypeVar`, `Generic`, and `Protocol`?

**Answer:**
```python
from typing import TypeVar, Generic, Protocol

# TypeVar — generic type parameter
T = TypeVar('T')

def first(lst: list[T]) -> T:
    return lst[0]

first([1, 2, 3])     # int
first(["a", "b"])     # str

# Generic — parameterized class
class Stack(Generic[T]):
    def __init__(self):
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

stack: Stack[int] = Stack()
stack.push(1)       # ✅ OK
# stack.push("a")   # mypy error

# Protocol — structural typing (duck typing + type safety)
class Serializable(Protocol):
    def to_json(self) -> str: ...

class User:
    def to_json(self) -> str:
        return '{"name": "Sid"}'

def save(obj: Serializable):  # Accepts anything with to_json()
    data = obj.to_json()

save(User())  # ✅ Works — User has to_json()
```

---

## 🔹 Section 6: Context Managers (Advanced)

### Q19. 🔴 Write a context manager for database transactions.

**Answer:**
```python
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

# Usage
with transaction(db_conn) as cursor:
    cursor.execute("INSERT INTO users VALUES (%s)", ("Sid",))
    cursor.execute("UPDATE accounts SET balance = balance - 100")
    # If ANY query fails → rollback ALL
```

---

### Q20. 🔴 What is `contextlib.AsyncExitStack`?

**Answer:**
```python
from contextlib import asynccontextmanager, AsyncExitStack

@asynccontextmanager
async def get_db():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

@asynccontextmanager
async def get_redis():
    client = await create_redis()
    try:
        yield client
    finally:
        await client.close()

# Manage multiple async resources
async def setup():
    async with AsyncExitStack() as stack:
        db = await stack.enter_async_context(get_db())
        redis = await stack.enter_async_context(get_redis())
        # Both cleaned up automatically
```

---

## 🔹 Section 7: Decorators (Advanced)

### Q21. 🔴 What is `functools.wraps` internally?

**Answer:**
`@wraps` copies `__name__`, `__doc__`, `__module__`, `__qualname__`, `__dict__`, and `__wrapped__`.

```python
from functools import wraps, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

print(WRAPPER_ASSIGNMENTS)
# ('__module__', '__name__', '__qualname__', '__annotations__',
#  '__doc__')

print(WRAPPER_UPDATES)
# ('__dict__',)

# @wraps internally uses functools.update_wrapper()
def my_decorator(func):
    @wraps(func)  # Same as: update_wrapper(wrapper, func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

### Q22. 🔴 Write a decorator that works with both sync and async functions.

**Answer:**
```python
import asyncio
from functools import wraps

def log_call(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        print(f"Calling async {func.__name__}")
        return await func(*args, **kwargs)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        print(f"Calling sync {func.__name__}")
        return func(*args, **kwargs)
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper

@log_call
def sync_func():
    return "sync"

@log_call
async def async_func():
    return "async"
```

---

## 🔹 Section 8: Python Internals

### Q23. 🔴 What happens when you do `import module`?

**Answer:**
```
1. Check sys.modules cache → return if found
2. Find the module (sys.path, finders)
3. Create module object
4. Add to sys.modules
5. Execute module code in module's namespace
6. Return module reference
```

```python
import sys

# Check if imported
"os" in sys.modules

# Import paths
print(sys.path)

# Force reimport
import importlib
importlib.reload(my_module)
```

---

### Q24. 🔴 What is `__all__`?

**Answer:**
Controls what `from module import *` exports.

```python
# utils.py
__all__ = ["public_func", "PublicClass"]

def public_func():
    pass

def _private_func():
    pass

class PublicClass:
    pass

class _PrivateClass:
    pass

# In another file:
from utils import *
# Only public_func and PublicClass are available
```

---

### Q25. 🔴 Explain Python's string interning and integer caching.

**Answer:**
```python
# Integer caching: -5 to 256
a = 256
b = 256
print(a is b)  # True (cached)

a = 257
b = 257
print(a is b)  # False (not cached)

# String interning: identifier-like strings
a = "hello"
b = "hello"
print(a is b)  # True (interned)

a = "hello world!"
b = "hello world!"
print(a is b)  # False (space + ! prevent interning)

# Force interning
import sys
a = sys.intern("hello world!")
b = sys.intern("hello world!")
print(a is b)  # True
```

---

## 🔹 Section 9: Tricky Questions

### Q26. 🔴 What is the output?

```python
import asyncio

async def f():
    return 42

result = f()
print(type(result))
print(result)
```

**Answer:**
```
<class 'coroutine'>
<coroutine object f at 0x...>
```
Plus a RuntimeWarning about coroutine never being awaited. Must use `await` or `asyncio.run()`.

---

### Q27. 🔴 What is the output?

```python
class A:
    def __init_subclass__(cls, **kwargs):
        print(f"Subclass created: {cls.__name__}")
        super().__init_subclass__(**kwargs)

class B(A):
    pass

class C(B):
    pass
```

**Answer:**
```
Subclass created: B
Subclass created: C
```
`__init_subclass__` is called whenever a class is subclassed.

---

### Q28. 🔴 What is the output?

```python
gen = (x for x in range(5))
print(list(gen))
print(list(gen))
```

**Answer:**
```
[0, 1, 2, 3, 4]
[]
```
Generators are exhausted after one pass.

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | Threading vs Multiprocessing? | I/O-bound vs CPU-bound |
| 2 | What is GIL? | One thread at a time in CPython |
| 3 | `async/await` purpose? | Non-blocking I/O concurrency |
| 4 | What is a metaclass? | Class of a class (`type`) |
| 5 | `__slots__` saves? | Memory (no `__dict__`) |
| 6 | Descriptor protocol? | `__get__`, `__set__`, `__delete__` |
| 7 | Weak reference purpose? | References that don't prevent GC |
| 8 | `asyncio.gather()` does? | Runs multiple coroutines concurrently |
| 9 | Type hint for optional? | `Optional[X]` or `X | None` |
| 10 | How to profile? | `cProfile`, `timeit`, `memory_profiler` |

---

*Next: [07_Database_ORM.md](07_Database_ORM.md)*
