# 01 — Python Core & Basics — Interview Questions

> **50+ questions covering Python fundamentals, memory model, GIL, CPython internals**

---

## 🔹 Section 1: Python Fundamentals

### Q1. 🟢 What is Python? Why is it popular for backend development?

**Answer:**
Python is a high-level, interpreted, dynamically-typed, general-purpose programming language.

**Popular for backend because:**
- Simple, readable syntax → faster development
- Rich ecosystem (Django, Flask, FastAPI)
- Strong community & library support
- Great for prototyping and MVPs
- Used by Google, Instagram, Spotify, Netflix

---

### Q2. 🟢 What is the difference between Python 2 and Python 3?

**Answer:**

| Feature | Python 2 | Python 3 |
|---------|----------|----------|
| Print | `print "hello"` | `print("hello")` |
| Division | `5/2 = 2` (integer) | `5/2 = 2.5` (float) |
| Strings | ASCII by default | Unicode by default |
| Range | `range()` returns list | `range()` returns iterator |
| Input | `raw_input()` | `input()` |
| Support | EOL (Jan 2020) | Active |

**Interview tip:** Python 2 is dead. Always say you work with Python 3.8+.

---

### Q3. 🟢 What are Python's key features?

**Answer:**
1. **Interpreted** — no compilation step needed
2. **Dynamically typed** — no need to declare types
3. **Object-oriented** — everything is an object
4. **Garbage collected** — automatic memory management
5. **Indentation-based** — uses whitespace for blocks
6. **Extensive standard library** — "batteries included"
7. **Cross-platform** — runs on Windows, Mac, Linux
8. **Duck typing** — "if it walks like a duck..."

---

### Q4. 🟢 What is PEP 8? Why is it important?

**Answer:**
PEP 8 is Python's official style guide.

**Key rules:**
```python
# Indentation: 4 spaces (NEVER tabs)
# Max line length: 79 characters
# Naming:
my_variable = 10        # snake_case for variables/functions
MY_CONSTANT = 3.14      # UPPER_SNAKE for constants
class MyClass:           # PascalCase for classes
    _private = "hidden"  # single underscore = internal
    __mangled = "name"   # double underscore = name mangling
```

**Why important:** Code consistency, readability, industry standard. Linters like `flake8` and `black` enforce it.

---

### Q5. 🟢 What is PEP? Name important PEPs.

**Answer:**
PEP = Python Enhancement Proposal. It's a design document for Python.

| PEP | Topic |
|-----|-------|
| PEP 8 | Style guide |
| PEP 20 | The Zen of Python (`import this`) |
| PEP 257 | Docstring conventions |
| PEP 484 | Type hints |
| PEP 572 | Walrus operator `:=` |
| PEP 634 | Structural pattern matching |
| PEP 3107 | Function annotations |

---

### Q6. 🟢 What is the difference between compiled and interpreted languages?

**Answer:**

| Compiled (C, Go, Rust) | Interpreted (Python, JS) |
|-------------------------|--------------------------|
| Converted to machine code before execution | Executed line by line at runtime |
| Faster execution | Slower execution |
| Errors caught at compile time | Errors caught at runtime |
| Platform-specific binary | Platform-independent |

**Python's reality:** Python is **both**. Source → compiled to bytecode (`.pyc`) → interpreted by PVM (Python Virtual Machine).

```
source.py → bytecode (.pyc) → PVM executes
```

---

### Q7. 🟢 What is `__pycache__`?

**Answer:**
A directory where Python stores compiled bytecode (`.pyc` files) to speed up subsequent imports. Created automatically.

```
__pycache__/
    module.cpython-311.pyc   # CPython 3.11 bytecode
```

- Regenerated when source changes
- Safe to delete (will be recreated)
- Always add to `.gitignore`

---

### Q8. 🟡 What is CPython? How is it different from Python?

**Answer:**
- **Python** = the language specification
- **CPython** = the default/reference implementation (written in C)

Other implementations:
| Implementation | Written In | Use Case |
|---------------|-----------|----------|
| **CPython** | C | Default, most libraries |
| **PyPy** | Python | Faster (JIT compiler) |
| **Jython** | Java | Runs on JVM |
| **IronPython** | C# | Runs on .NET |
| **MicroPython** | C | IoT / embedded |

**Interview tip:** When someone says "Python," they almost always mean CPython.

---

## 🔹 Section 2: Variables & Data Types

### Q9. 🟢 What are Python's built-in data types?

**Answer:**

| Category | Types |
|----------|-------|
| **Numeric** | `int`, `float`, `complex`, `bool` |
| **Sequence** | `str`, `list`, `tuple`, `range` |
| **Mapping** | `dict` |
| **Set** | `set`, `frozenset` |
| **Binary** | `bytes`, `bytearray`, `memoryview` |
| **None** | `NoneType` |

---

### Q10. 🟢 What is the difference between mutable and immutable types?

**Answer:**

| Mutable (can change) | Immutable (cannot change) |
|----------------------|--------------------------|
| `list` | `tuple` |
| `dict` | `str` |
| `set` | `int`, `float` |
| `bytearray` | `frozenset`, `bytes` |

```python
# Immutable — creates new object
x = "hello"
x = x + " world"  # new string object created

# Mutable — modifies in place
lst = [1, 2, 3]
lst.append(4)      # same object modified
```

**Why it matters for backend:**
- Immutable types are hashable → can be dict keys
- Mutable default arguments are a common bug

---

### Q11. 🟡 What is the mutable default argument trap?

**Answer:**
```python
# ❌ BUG: Default list is shared across ALL calls
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2] — NOT [2]!

# ✅ FIX: Use None as default
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

**Why?** Default values are evaluated ONCE at function definition, not at each call.

---

### Q12. 🟢 What is the difference between `is` and `==`?

**Answer:**
```python
# == checks VALUE equality
# is checks IDENTITY (same object in memory)

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  (same values)
print(a is b)   # False (different objects)
print(a is c)   # True  (same object)
```

**Integer caching (important!):**
```python
x = 256
y = 256
print(x is y)  # True — CPython caches -5 to 256

x = 257
y = 257
print(x is y)  # False — outside cache range
```

**Rule:** Always use `==` for value comparison. Only use `is` for `None` checks: `if x is None`.

---

### Q13. 🟢 What is `None` in Python?

**Answer:**
- `None` is Python's null value
- It's a singleton (only one `None` object exists)
- Type is `NoneType`
- Evaluates to `False` in boolean context

```python
x = None
print(type(x))       # <class 'NoneType'>
print(x is None)     # True  ✅ (preferred)
print(x == None)     # True  ❌ (works but not recommended)
print(bool(None))    # False
```

---

### Q14. 🟡 What is string interning?

**Answer:**
Python caches small/simple strings in memory for reuse.

```python
a = "hello"
b = "hello"
print(a is b)  # True — interned

a = "hello world!"
b = "hello world!"
print(a is b)  # False — not interned (has space and !)
```

**Interning rules (CPython):**
- Strings that look like identifiers are interned
- Compile-time strings may be interned
- Use `sys.intern()` to force interning

---

### Q15. 🟢 What is type conversion? Implicit vs Explicit?

**Answer:**
```python
# Implicit (Python does it automatically)
x = 5 + 2.0    # int + float → float (7.0)
y = True + 1    # bool + int → int (2)

# Explicit (you do it manually)
int("42")       # str → int
float("3.14")   # str → float
str(100)        # int → str
list("abc")     # str → list ['a', 'b', 'c']
tuple([1,2,3])  # list → tuple
set([1,1,2])    # list → set {1, 2}
```

---

## 🔹 Section 3: Memory Management

### Q16. 🟡 How does Python manage memory?

**Answer:**
Python uses a **private heap** managed by the Python Memory Manager:

1. **Memory Allocator** — allocates memory from OS
2. **Object-specific allocators** — optimized for small objects
3. **Reference counting** — primary garbage collection
4. **Generational GC** — handles circular references

```
┌─────────────────────────────┐
│     Python Memory Manager    │
├─────────────────────────────┤
│   Object-specific allocators │
│   (int, list, dict, etc.)   │
├─────────────────────────────┤
│      PyMalloc (< 512 bytes) │
├─────────────────────────────┤
│     C malloc / OS memory     │
└─────────────────────────────┘
```

---

### Q17. 🟡 What is reference counting?

**Answer:**
Every Python object has a reference count. When it reaches 0, the object is immediately deallocated.

```python
import sys

a = [1, 2, 3]        # ref count = 1
b = a                 # ref count = 2
print(sys.getrefcount(a))  # 3 (includes temp ref from getrefcount)

del b                 # ref count = 1
del a                 # ref count = 0 → FREED
```

**Limitations:** Cannot detect circular references.
```python
a = []
b = []
a.append(b)  # a → b
b.append(a)  # b → a (circular!)
# Reference count never reaches 0
```

---

### Q18. 🟡 What is the garbage collector in Python?

**Answer:**
Python has TWO garbage collection mechanisms:

1. **Reference counting** (primary) — immediate, deterministic
2. **Generational GC** (secondary) — handles cycles

**Generational GC:**
- 3 generations (0, 1, 2)
- New objects start in Gen 0
- Objects that survive collection are promoted
- Gen 0 collected most frequently, Gen 2 least

```python
import gc

gc.get_count()       # (gen0, gen1, gen2) counts
gc.collect()         # Force collection
gc.disable()         # Disable GC (not recommended)
gc.get_threshold()   # (700, 10, 10) default thresholds
```

---

### Q19. 🔴 What is the GIL (Global Interpreter Lock)?

**Answer:**
The GIL is a mutex that allows only ONE thread to execute Python bytecode at a time, even on multi-core CPUs.

**Why it exists:**
- CPython's memory management (reference counting) is NOT thread-safe
- GIL makes single-threaded programs faster
- Simplifies C extension development

**Impact:**
```python
# ❌ CPU-bound — GIL is a bottleneck
import threading
# Two threads fighting for one GIL = no parallel execution

# ✅ I/O-bound — GIL is released during I/O
# Network calls, file reads → threads work fine

# ✅ CPU-bound solution → use multiprocessing
from multiprocessing import Pool
# Each process has its own GIL
```

**Key interview points:**
- GIL is a CPython limitation, not a Python language limitation
- PyPy and Jython don't have a GIL
- Python 3.12: Per-interpreter GIL (PEP 684)
- Python 3.13: Experimental free-threaded build (no-GIL)

---

### Q20. 🔴 How do you bypass the GIL?

**Answer:**

| Method | Use Case |
|--------|----------|
| `multiprocessing` | CPU-bound tasks (separate processes) |
| `asyncio` | I/O-bound tasks (single-threaded) |
| C extensions | NumPy releases GIL during computation |
| `concurrent.futures` | High-level API for both |
| Cython + `nogil` | Release GIL in Cython code |
| `subprocess` | Run external processes |

```python
# Multiprocessing for CPU-bound
from multiprocessing import Pool

def heavy_computation(n):
    return sum(i * i for i in range(n))

with Pool(4) as pool:
    results = pool.map(heavy_computation, [10**6] * 4)
```

---

## 🔹 Section 4: Scope & Namespaces

### Q21. 🟢 What is the LEGB rule?

**Answer:**
Python resolves variable names in this order:

```
L — Local      (inside current function)
E — Enclosing  (inside enclosing function — closures)
G — Global     (module level)
B — Built-in   (Python's built-in names)
```

```python
x = "global"                  # G

def outer():
    x = "enclosing"           # E
    
    def inner():
        x = "local"           # L
        print(x)              # "local" ← L wins
    
    inner()

outer()
print(len)                    # <built-in function len> ← B
```

---

### Q22. 🟡 What is the difference between `global` and `nonlocal`?

**Answer:**
```python
x = 10

def outer():
    y = 20
    
    def inner():
        global x       # Refers to module-level x
        nonlocal y     # Refers to enclosing function's y
        x = 100
        y = 200
    
    inner()
    print(y)  # 200 (changed by nonlocal)

outer()
print(x)      # 100 (changed by global)
```

| Keyword | Refers To | Use Case |
|---------|-----------|----------|
| `global` | Module-level variable | Modify global from function |
| `nonlocal` | Enclosing function variable | Modify closure variable |

**Backend tip:** Avoid `global` in production code. Use classes, config objects, or dependency injection instead.

---

### Q23. 🟡 What are namespaces in Python?

**Answer:**
A namespace is a mapping from names to objects (like a dictionary).

| Namespace | Created At | Destroyed At |
|-----------|-----------|--------------|
| **Built-in** | Python starts | Python exits |
| **Global** | Module loaded | Module unloaded |
| **Local** | Function called | Function returns |
| **Enclosing** | Enclosing function called | Enclosing function returns |

```python
# See all names in a namespace
print(dir())              # Current namespace
print(dir(__builtins__))  # Built-in namespace
print(globals())          # Global namespace dict
print(locals())           # Local namespace dict
```

---

## 🔹 Section 5: Python Internals

### Q24. 🟡 What is `__init__.py`? What is its purpose?

**Answer:**
```
mypackage/
    __init__.py      # Makes directory a Python package
    module_a.py
    module_b.py
```

**Old Python (< 3.3):** Required for directory to be a package.
**Python 3.3+:** Optional (namespace packages exist), but still recommended.

**Uses:**
```python
# __init__.py can:
# 1. Be empty (just marks as package)
# 2. Define __all__ for star imports
__all__ = ["module_a", "module_b"]

# 3. Run initialization code
print("Package loaded!")

# 4. Provide convenient imports
from .module_a import ClassA
from .module_b import ClassB
```

---

### Q25. 🟡 What is `__name__` and `__main__`?

**Answer:**
```python
# my_module.py
print(f"__name__ = {__name__}")

def main():
    print("Running as main script")

if __name__ == "__main__":
    main()
```

| How You Run | `__name__` Value |
|-------------|-----------------|
| `python my_module.py` | `"__main__"` |
| `import my_module` | `"my_module"` |

**Why it matters:** Prevents code from running when the module is imported.

---

### Q26. 🟡 What are dunder (magic) methods? Name the most important ones.

**Answer:**
Dunder = Double UNDERscore. They're special methods Python calls automatically.

| Method | Called When | Example |
|--------|-----------|---------|
| `__init__` | Object creation | `obj = MyClass()` |
| `__str__` | `str(obj)` / `print(obj)` | Human-readable |
| `__repr__` | `repr(obj)` / debugger | Developer-readable |
| `__len__` | `len(obj)` | `len(my_list)` |
| `__getitem__` | `obj[key]` | `my_dict["key"]` |
| `__setitem__` | `obj[key] = val` | `my_dict["key"] = 1` |
| `__contains__` | `item in obj` | `"a" in my_list` |
| `__eq__` | `obj1 == obj2` | Equality check |
| `__hash__` | `hash(obj)` | Dict key / set member |
| `__call__` | `obj()` | Make object callable |
| `__enter__`/`__exit__` | `with` statement | Context manager |
| `__iter__`/`__next__` | `for x in obj` | Iteration |
| `__add__` | `obj1 + obj2` | Operator overloading |

---

### Q27. 🟡 What is the difference between `__str__` and `__repr__`?

**Answer:**
```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name} (age {self.age})"   # For users
    
    def __repr__(self):
        return f"User(name='{self.name}', age={self.age})"  # For developers

u = User("Sid", 25)
print(str(u))    # Sid (age 25)
print(repr(u))   # User(name='Sid', age=25)
print(u)         # Sid (age 25) — print calls __str__
print([u])       # [User(name='Sid', age=25)] — list calls __repr__
```

**Rule:** `__repr__` should ideally be valid Python that recreates the object.

---

### Q28. 🟡 What are `*args` and `**kwargs`?

**Answer:**
```python
# *args  → collects positional arguments into a tuple
# **kwargs → collects keyword arguments into a dict

def example(*args, **kwargs):
    print(f"args: {args}")       # tuple
    print(f"kwargs: {kwargs}")   # dict

example(1, 2, 3, name="Sid", age=25)
# args: (1, 2, 3)
# kwargs: {'name': 'Sid', 'age': 25}

# Unpacking
def greet(name, age):
    print(f"Hi {name}, age {age}")

data = {"name": "Sid", "age": 25}
greet(**data)  # Hi Sid, age 25

nums = [1, 2]
greet(*nums)   # Error (expects name, age — not 2 ints)
```

**Backend use:** Very common in decorators and wrapper functions.

---

### Q29. 🟡 What is the difference between `deepcopy` and `shallow copy`?

**Answer:**
```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy — copies outer list, but inner lists are SHARED
shallow = copy.copy(original)
shallow[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] ← CHANGED!

# Deep copy — copies everything recursively
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0].append(99)
print(original)  # [[1, 2], [3, 4]] ← NOT changed
```

| Method | What It Copies | Nested Objects |
|--------|---------------|----------------|
| `=` | Reference only | Shared |
| `copy.copy()` | Top-level only | Shared |
| `copy.deepcopy()` | Everything | Independent |

---

### Q30. 🟢 What are f-strings? Why prefer them?

**Answer:**
```python
name = "Sid"
age = 25

# f-string (Python 3.6+) — FASTEST & most readable
print(f"Hi {name}, age {age}")
print(f"{2 + 3 = }")          # "2 + 3 = 5" (debug format, 3.8+)
print(f"{name!r}")             # "'Sid'" (repr)
print(f"{3.14159:.2f}")        # "3.14" (format spec)
print(f"{1000000:,}")          # "1,000,000" (comma separator)

# Old methods (still seen in codebases)
print("Hi %s, age %d" % (name, age))        # % formatting
print("Hi {}, age {}".format(name, age))     # .format()
```

**Why f-strings are best:**
- Fastest performance
- Most readable
- Inline expressions
- Format spec support

---

## 🔹 Section 6: Comparison & Tricky Questions

### Q31. 🟢 What is the difference between `list` and `tuple`?

**Answer:**

| Feature | List | Tuple |
|---------|------|-------|
| Mutable | ✅ Yes | ❌ No |
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
| Hashable | ❌ No | ✅ Yes (if elements are) |
| Performance | Slower | Faster |
| Memory | More | Less |
| Use case | Collection that changes | Fixed data, dict keys |

---

### Q32. 🟢 What is the difference between `append()` and `extend()`?

**Answer:**
```python
lst = [1, 2, 3]

lst.append([4, 5])   # Adds as single element
print(lst)            # [1, 2, 3, [4, 5]]

lst = [1, 2, 3]
lst.extend([4, 5])   # Adds each element
print(lst)            # [1, 2, 3, 4, 5]
```

---

### Q33. 🟡 What happens when you do `a = 256` vs `a = 257`?

**Answer:**
```python
# CPython caches integers from -5 to 256
a = 256
b = 256
print(a is b)  # True — same cached object

a = 257
b = 257
print(a is b)  # False — different objects
# (may be True in interactive mode due to compiler optimizations)
```

**Why?** Performance optimization. Small integers are used frequently.

---

### Q34. 🟡 What is the output?

```python
print(0.1 + 0.2 == 0.3)
```

**Answer:** `False`

```python
print(0.1 + 0.2)         # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False

# Fix: Use decimal or math.isclose
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True

import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

**Why?** Floating-point numbers use IEEE 754 binary representation. Not all decimals can be represented exactly.

---

### Q35. 🟡 What is the output?

```python
print(bool(""))
print(bool(0))
print(bool([]))
print(bool(None))
print(bool("0"))
print(bool(" "))
```

**Answer:**
```python
print(bool(""))     # False — empty string
print(bool(0))      # False — zero
print(bool([]))     # False — empty list
print(bool(None))   # False — None
print(bool("0"))    # True  — non-empty string!
print(bool(" "))    # True  — non-empty string!
```

**Falsy values:** `False`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `0j`

---

### Q36. 🟡 What is the output?

```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
```

**Answer:** `[1, 2, 3, 4]`

Because `y = x` copies the **reference**, not the list. Both `x` and `y` point to the same list object.

---

### Q37. 🔴 What is the output?

```python
def f(x, lst=[]):
    lst.append(x)
    return lst

print(f(1))
print(f(2))
print(f(3))
```

**Answer:**
```
[1]
[1, 2]
[1, 2, 3]
```

The default list is created once and shared across calls (mutable default argument trap).

---

### Q38. 🟡 What is the output?

```python
a = [1, 2, 3, 4, 5]
print(a[10:])
```

**Answer:** `[]` — Slicing NEVER raises IndexError, it returns empty list.

```python
a = [1, 2, 3, 4, 5]
print(a[10:])   # []
print(a[10])    # IndexError: list index out of range
```

---

## 🔹 Section 7: Important Concepts

### Q39. 🟡 What is duck typing?

**Answer:**
"If it walks like a duck and quacks like a duck, it's a duck."

Python doesn't check types — it checks behavior.

```python
class Duck:
    def quack(self):
        print("Quack!")

class Person:
    def quack(self):
        print("I'm quacking like a duck!")

def make_it_quack(thing):
    thing.quack()  # Don't care about type, just behavior

make_it_quack(Duck())    # Quack!
make_it_quack(Person())  # I'm quacking like a duck!
```

---

### Q40. 🟡 What is monkey patching?

**Answer:**
Modifying classes or modules at runtime.

```python
class MyClass:
    def greet(self):
        return "Hello"

obj = MyClass()
print(obj.greet())  # Hello

# Monkey patch
def new_greet(self):
    return "Hey there!"

MyClass.greet = new_greet
print(obj.greet())  # Hey there!
```

**Backend use:** Commonly used in testing (mocking). Avoid in production — makes code unpredictable.

---

### Q41. 🟡 What is the difference between `del`, `remove()`, and `pop()`?

**Answer:**
```python
lst = [10, 20, 30, 40, 50]

del lst[1]         # Delete by INDEX → [10, 30, 40, 50]
lst.remove(30)     # Delete by VALUE (first occurrence) → [10, 40, 50]
x = lst.pop(1)     # Delete by INDEX and RETURN → x=40, [10, 50]
lst.pop()          # Remove LAST element → [10]
lst.clear()        # Remove ALL → []
```

| Method | By | Returns | Raises |
|--------|----|---------|--------|
| `del lst[i]` | Index | Nothing | IndexError |
| `lst.remove(val)` | Value | Nothing | ValueError |
| `lst.pop(i)` | Index | Removed item | IndexError |

---

### Q42. 🟡 What are list comprehensions? When should you NOT use them?

**Answer:**
```python
# List comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested
matrix = [[i*j for j in range(3)] for i in range(3)]

# Dict comprehension
word_len = {w: len(w) for w in ["hello", "world"]}

# Set comprehension
unique = {x % 5 for x in range(20)}
```

**DON'T use when:**
- Logic is complex (> 1 condition) → use regular loop
- You need side effects (printing, writing) → use loop
- Result is huge → use generator expression instead
- Readability suffers

```python
# ❌ Too complex
result = [x for x in data if x > 0 for y in x.items() if y[1] > threshold]

# ✅ Use a loop instead
result = []
for x in data:
    if x > 0:
        for y in x.items():
            if y[1] > threshold:
                result.append(x)
```

---

### Q43. 🟡 What is the difference between a generator and a list comprehension?

**Answer:**
```python
# List comprehension — stores ALL values in memory
lst = [x**2 for x in range(1000000)]     # ~8MB in memory

# Generator expression — produces values on demand
gen = (x**2 for x in range(1000000))     # ~120 bytes!
```

| Feature | List Comprehension | Generator |
|---------|-------------------|-----------|
| Syntax | `[...]` | `(...)` |
| Memory | All in memory | One at a time |
| Speed | Faster for small data | Better for large data |
| Reusable | Yes | No (exhausted after one pass) |
| Indexable | Yes `lst[5]` | No |

---

### Q44. 🟢 What is `enumerate()`? Why use it?

**Answer:**
```python
fruits = ["apple", "banana", "cherry"]

# ❌ Without enumerate
for i in range(len(fruits)):
    print(i, fruits[i])

# ✅ With enumerate — Pythonic!
for i, fruit in enumerate(fruits):
    print(i, fruit)

# Custom start index
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)  # 1 apple, 2 banana, 3 cherry
```

---

### Q45. 🟢 What is `zip()`? What happens with unequal lengths?

**Answer:**
```python
names = ["Sid", "Raj", "Amit"]
ages = [25, 30, 28]

# zip combines into tuples
for name, age in zip(names, ages):
    print(f"{name}: {age}")

# Unequal lengths — stops at shortest
names = ["Sid", "Raj", "Amit"]
ages = [25, 30]
list(zip(names, ages))  # [('Sid', 25), ('Raj', 30)] — "Amit" dropped

# zip_longest — fills missing with default
from itertools import zip_longest
list(zip_longest(names, ages, fillvalue=0))
# [('Sid', 25), ('Raj', 30), ('Amit', 0)]
```

---

## 🔹 Section 8: Practical Backend Questions

### Q46. 🟡 How do you handle environment variables in Python?

**Answer:**
```python
import os

# Read
db_url = os.environ.get("DATABASE_URL", "sqlite:///default.db")
secret = os.environ["SECRET_KEY"]  # Raises KeyError if missing

# Set (for current process only)
os.environ["MY_VAR"] = "value"

# Best practice: use python-dotenv
# pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()  # Loads from .env file

db_url = os.getenv("DATABASE_URL")
```

**.env file:**
```
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=super-secret-key
DEBUG=True
```

---

### Q47. 🟡 What is `if __name__ == "__main__"`? Why is it important?

**Answer:**
```python
# utils.py
def calculate(x):
    return x * 2

if __name__ == "__main__":
    # Only runs when script is executed directly
    print(calculate(5))  # 10
    
# When imported: import utils → this block does NOT run
# When run: python utils.py → this block RUNS
```

**Backend importance:** Lets you have utility scripts that can both be imported AND run standalone.

---

### Q48. 🟡 What are virtual environments? Why are they essential?

**Answer:**
Virtual environments provide isolated Python environments per project.

```bash
# Create
python -m venv myenv

# Activate
source myenv/bin/activate     # macOS/Linux
myenv\Scripts\activate        # Windows

# Install packages (isolated)
pip install django flask

# Freeze requirements
pip freeze > requirements.txt

# Deactivate
deactivate
```

**Why essential for backend:**
- Project A needs Django 3.2, Project B needs Django 4.2
- Reproducible deployments (`requirements.txt`)
- No conflicts between projects
- Clean production environments

---

### Q49. 🟡 What are `requirements.txt` vs `pyproject.toml` vs `Pipfile`?

**Answer:**

| File | Tool | Format |
|------|------|--------|
| `requirements.txt` | pip | `package==version` |
| `pyproject.toml` | pip/setuptools/poetry | TOML standard |
| `Pipfile` | pipenv | TOML-like |
| `setup.py` | setuptools (old) | Python script |

```
# requirements.txt
django==4.2.7
celery==5.3.4
redis>=4.0,<5.0

# pyproject.toml (modern standard)
[project]
dependencies = [
    "django>=4.2",
    "celery>=5.3",
]
```

**Recommendation:** Use `requirements.txt` for simple projects, `pyproject.toml` for libraries/modern projects.

---

### Q50. 🟡 What is the walrus operator `:=`?

**Answer:**
Assignment expression (Python 3.8+) — assigns and returns value in one step.

```python
# Without walrus
line = input()
while line != "quit":
    process(line)
    line = input()

# With walrus ✅
while (line := input()) != "quit":
    process(line)

# In list comprehension
data = [1, 5, 3, 8, 2, 9]
results = [y for x in data if (y := x * 2) > 6]
# results = [10, 16, 18]

# In if statements
if (n := len(my_list)) > 10:
    print(f"List is too long ({n} elements)")
```

---

### Q51. 🔴 What is the difference between `__new__` and `__init__`?

**Answer:**
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        # __new__ CREATES the object (called first)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # __init__ INITIALIZES the object (called second)
        self.value = 42

a = Singleton()
b = Singleton()
print(a is b)  # True — same instance
```

| Method | Purpose | Returns |
|--------|---------|---------|
| `__new__` | Creates instance | Must return instance |
| `__init__` | Initializes instance | Returns `None` |

**When to override `__new__`:** Singleton pattern, immutable types, metaclasses.

---

### Q52. 🔴 Explain Python's method resolution order (MRO).

**Answer:**
MRO determines the order in which base classes are searched when calling a method.

```python
class A:
    def who(self): return "A"

class B(A):
    def who(self): return "B"

class C(A):
    def who(self): return "C"

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

print(D().who())  # "B" — follows MRO: D → B → C → A
```

Python uses **C3 Linearization** algorithm for MRO.

**Rule:** A class always appears before its parents, and the order of parents is preserved.

---

### Q53. 🟡 What is `pass`, `continue`, `break`, and `else` in loops?

**Answer:**
```python
# pass — do nothing (placeholder)
class MyClass:
    pass

# break — exit the loop
for i in range(10):
    if i == 5:
        break      # stops at 5

# continue — skip current iteration
for i in range(10):
    if i % 2 == 0:
        continue   # skips even numbers
    print(i)       # 1, 3, 5, 7, 9

# else in loop — runs if loop completed WITHOUT break
for i in range(10):
    if i == 99:
        break
else:
    print("Loop completed normally!")  # This prints
```

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | Is Python compiled or interpreted? | Both — compiled to bytecode, then interpreted |
| 2 | What is GIL? | Mutex allowing one thread at a time in CPython |
| 3 | `is` vs `==`? | `is` = identity, `==` = equality |
| 4 | Mutable types? | list, dict, set, bytearray |
| 5 | What is `self`? | Reference to current instance |
| 6 | `*args` vs `**kwargs`? | Positional tuple vs keyword dict |
| 7 | How to copy a list? | `lst.copy()`, `lst[:]`, `list(lst)`, `copy.deepcopy()` |
| 8 | What is PEP 8? | Python style guide |
| 9 | What is `None`? | Python's null singleton |
| 10 | Smallest integer cached? | -5 to 256 in CPython |

---

*Next: [02_Data_Structures.md](02_Data_Structures.md)*
