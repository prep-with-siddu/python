# 13 — Python Gotchas & Tricky Output — Interview Questions

> **60+ tricky questions that interviewers LOVE to ask — mutable defaults, closures, scoping, is vs ==, and deep Python internals**

---

## 🔹 Section 1: Mutable Default Arguments (TOP 1 GOTCHA)

### Q1. 🟡 What is the output?

```python
def append_to(element, target=[]):
    target.append(element)
    return target

print(append_to(1))
print(append_to(2))
print(append_to(3))
```

**Answer:**
```
[1]
[1, 2]
[1, 2, 3]
```

**Why?** Default mutable arguments are created **once** when the function is defined, not each call. All calls share the **same list object**.

**Fix:**
```python
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

print(append_to(1))  # [1]
print(append_to(2))  # [2]  ← Fresh list each time
```

---

### Q2. 🟡 What is the output?

```python
def create_multipliers():
    return [lambda x: x * i for i in range(5)]

for multiplier in create_multipliers():
    print(multiplier(2), end=" ")
```

**Answer:**
```
8 8 8 8 8
```

**Why?** Late binding closure — `i` is looked up when the lambda is **called**, not when it's **defined**. By then, `i = 4`.

**Fix:**
```python
# Fix 1: Default argument (captures value at definition time)
def create_multipliers():
    return [lambda x, i=i: x * i for i in range(5)]
# Output: 0 2 4 6 8

# Fix 2: functools.partial
from functools import partial
def create_multipliers():
    return [partial(lambda i, x: x * i, i) for i in range(5)]
```

---

### Q3. 🟡 What is the output?

```python
class MyClass:
    items = []
    
    def add(self, item):
        self.items.append(item)

a = MyClass()
b = MyClass()
a.add("hello")
print(b.items)
```

**Answer:**
```
['hello']
```

**Why?** `items = []` is a **class variable**, shared by all instances. Both `a` and `b` point to the **same list**.

**Fix:**
```python
class MyClass:
    def __init__(self):
        self.items = []  # Instance variable — unique per object
```

---

## 🔹 Section 2: `is` vs `==` Gotchas

### Q4. 🟢 What is the output?

```python
a = 256
b = 256
print(a is b)

c = 257
d = 257
print(c is d)
```

**Answer:**
```
True
False  (in most cases)
```

**Why?** CPython caches integers from **-5 to 256** (small integer pool). So `a` and `b` point to the same object. `257` is outside the pool, so `c` and `d` are different objects.

**Rule:** Use `==` for value, `is` for identity (same object).

---

### Q5. 🟡 What is the output?

```python
a = "hello"
b = "hello"
print(a is b)

c = "hello world"
d = "hello world"
print(c is d)

e = "hello_world"
f = "hello_world"
print(e is f)
```

**Answer:**
```
True
False  (may vary)
True
```

**Why?** CPython **interns** strings that look like identifiers (alphanumeric + underscore). `"hello"` and `"hello_world"` are interned. `"hello world"` (with space) is NOT.

---

### Q6. 🟡 What is the output?

```python
print([] == [])
print([] is [])

print("" == "")
print("" is "")

print(() == ())
print(() is ())
```

**Answer:**
```
True
False   ← Two different list objects

True
True    ← Empty string is interned

True
True    ← Empty tuple is cached (immutable singleton)
```

---

## 🔹 Section 3: Scope & Variable Gotchas

### Q7. 🟡 What is the output?

```python
x = 10

def foo():
    print(x)
    x = 20

foo()
```

**Answer:**
```
UnboundLocalError: local variable 'x' referenced before assignment
```

**Why?** Python scans the entire function body at compile time. Since `x = 20` exists, `x` is treated as **local** throughout the function. The `print(x)` runs before `x = 20`.

**Fix:** Use `global x` or restructure the code.

---

### Q8. 🟡 What is the output?

```python
x = [1, 2, 3]

def foo():
    x.append(4)
    print(x)

foo()
print(x)
```

**Answer:**
```
[1, 2, 3, 4]
[1, 2, 3, 4]
```

**Why?** No `x = ...` in `foo()`, so Python looks up `x` in the enclosing scope. Lists are mutable — `.append()` modifies in place, no reassignment needed.

---

### Q9. 🔴 What is the output?

```python
def outer():
    x = 10
    def inner():
        x += 1
        return x
    return inner()

print(outer())
```

**Answer:**
```
UnboundLocalError: local variable 'x' referenced before assignment
```

**Why?** `x += 1` is `x = x + 1` — assignment makes `x` local to `inner()`. Same as Q7.

**Fix:**
```python
def outer():
    x = 10
    def inner():
        nonlocal x  # Now refers to outer's x
        x += 1
        return x
    return inner()

print(outer())  # 11
```

---

### Q10. 🟡 What is the output?

```python
for i in range(3):
    pass

print(i)
```

**Answer:**
```
2
```

**Why?** In Python, `for` loop variables **leak** into the enclosing scope. After the loop, `i` still exists with its last value.

---

## 🔹 Section 4: Tuple & Immutability Gotchas

### Q11. 🟡 What is the output?

```python
t = (1, 2, [3, 4])
t[2].append(5)
print(t)
```

**Answer:**
```
(1, 2, [3, 4, 5])
```

**Why?** Tuples are immutable — you can't change which objects they reference. But the **list inside** is still mutable. The tuple holds a reference to the list, and the list itself can change.

---

### Q12. 🟡 What is the output?

```python
t = (1, 2, [3, 4])
t[2] += [5, 6]
```

**Answer:**
```
TypeError: 'tuple' object does not support item assignment
```

**BUT** `t[2]` is now `[3, 4, 5, 6]`! 

**Why?** `t[2] += [5, 6]` does TWO things:
1. `t[2].extend([5, 6])` — **succeeds** (mutates the list)
2. `t[2] = result` — **fails** (tuple assignment)

So the list IS modified, but the assignment raises an error.

---

### Q13. 🟢 What is the output?

```python
a = (1)
b = (1,)
print(type(a))
print(type(b))
```

**Answer:**
```
<class 'int'>
<class 'tuple'>
```

**Why?** `(1)` is just parentheses around an integer. You need the **trailing comma** `(1,)` to make a single-element tuple.

---

## 🔹 Section 5: Dictionary & Iteration Gotchas

### Q14. 🟡 What is the output?

```python
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    if key == "b":
        del d[key]
```

**Answer:**
```
RuntimeError: dictionary changed size during iteration
```

**Fix:**
```python
# Create a copy of keys
for key in list(d.keys()):
    if key == "b":
        del d[key]

# Or use dict comprehension
d = {k: v for k, v in d.items() if k != "b"}
```

---

### Q15. 🟡 What is the output?

```python
d = {}
d[True] = "yes"
d[1] = "one"
d[1.0] = "float_one"

print(d)
print(len(d))
```

**Answer:**
```
{True: 'float_one'}
1
```

**Why?** In Python `True == 1 == 1.0` and `hash(True) == hash(1) == hash(1.0)`. They're the **same key**. The first key `True` is kept, but the value gets overwritten each time.

---

### Q16. 🟡 What is the output?

```python
keys = [1, 2, 3]
values = ['a', 'b', 'c', 'd']

d = dict(zip(keys, values))
print(d)
```

**Answer:**
```
{1: 'a', 2: 'b', 3: 'c'}
```

**Why?** `zip` stops at the shortest iterable. `'d'` is ignored.

---

## 🔹 Section 6: String & Number Gotchas

### Q17. 🟡 What is the output?

```python
print(0.1 + 0.2 == 0.3)
print(0.1 + 0.2)
```

**Answer:**
```
False
0.30000000000000004
```

**Why?** Floating-point arithmetic (IEEE 754) cannot represent 0.1 and 0.2 exactly in binary.

**Fix:**
```python
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))  # True

# Or use math.isclose
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

---

### Q18. 🟢 What is the output?

```python
print(bool(""))
print(bool(" "))
print(bool("0"))
print(bool("False"))
print(bool([]))
print(bool([0]))
print(bool(0))
print(bool(None))
```

**Answer:**
```
False    ← Empty string
True     ← Space is a character
True     ← "0" is a non-empty string
True     ← "False" is a non-empty string!
False    ← Empty list
True     ← List with one element
False    ← Zero
False    ← None
```

**Falsy values:** `None`, `False`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`, `frozenset()`

---

### Q19. 🟡 What is the output?

```python
print("abc" * 0)
print("abc" * -1)
print([1, 2] * 0)
```

**Answer:**
```
""       ← empty string
""       ← empty string (negative = 0)
[]       ← empty list
```

---

### Q20. 🟡 What is the output?

```python
a = [0] * 3
print(a)

b = [[0]] * 3
b[0].append(1)
print(b)
```

**Answer:**
```
[0, 0, 0]
[[0, 1], [0, 1], [0, 1]]
```

**Why?** `[[0]] * 3` creates 3 references to the **same inner list**. Modifying one modifies all.

**Fix:**
```python
b = [[0] for _ in range(3)]  # 3 separate lists
b[0].append(1)
print(b)  # [[0, 1], [0], [0]]
```

---

## 🔹 Section 7: Class & OOP Gotchas

### Q21. 🟡 What is the output?

```python
class A:
    def __init__(self):
        print("A", end=" ")

class B(A):
    pass

class C(A):
    def __init__(self):
        print("C", end=" ")

class D(B, C):
    pass

d = D()
print()
print(D.__mro__)
```

**Answer:**
```
C
(<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

**Why?** MRO (C3 linearization): D → B → C → A. Since `B` doesn't have `__init__`, it goes to next in MRO = `C`. `C.__init__` is called (which doesn't call `super()`).

---

### Q22. 🟡 What is the output?

```python
class Parent:
    x = 1

class Child(Parent):
    pass

class GrandChild(Child):
    pass

print(Parent.x, Child.x, GrandChild.x)

Child.x = 2
print(Parent.x, Child.x, GrandChild.x)
```

**Answer:**
```
1 1 1
1 2 2
```

**Why?** Initially all share `Parent.x`. After `Child.x = 2`, `Child` gets its own `x`. `GrandChild` inherits from `Child`, so it sees `2`. `Parent.x` is unaffected.

---

### Q23. 🟡 What is the output?

```python
class Foo:
    def __repr__(self):
        return "Foo()"
    
    def __str__(self):
        return "I am Foo"

f = Foo()
print(f)
print([f])
print(f"{f}")
```

**Answer:**
```
I am Foo     ← print() uses __str__
[Foo()]      ← Inside a list, __repr__ is used
I am Foo     ← f-string uses __str__
```

---

### Q24. 🔴 What is the output?

```python
class Meta(type):
    def __new__(cls, name, bases, namespace):
        print(f"Creating class: {name}")
        return super().__new__(cls, name, bases, namespace)

class MyClass(metaclass=Meta):
    pass

class Child(MyClass):
    pass
```

**Answer:**
```
Creating class: MyClass
Creating class: Child
```

**Why?** Metaclass `__new__` is called when the **class** is created (not when instances are created). Both `MyClass` and `Child` trigger it.

---

## 🔹 Section 8: Import & Module Gotchas

### Q25. 🟡 What happens with circular imports?

```python
# a.py
from b import func_b
def func_a():
    return "A"

# b.py
from a import func_a
def func_b():
    return "B"

# Running a.py gives:
# ImportError: cannot import name 'func_a' from partially initialized module 'a'
```

**Fix:**
```python
# Option 1: Import inside function (lazy import)
# b.py
def func_b():
    from a import func_a
    return "B"

# Option 2: Import the module, not the name
# b.py
import a
def func_b():
    a.func_a()

# Option 3: Restructure code (best)
```

---

### Q26. 🟡 What is `if __name__ == "__main__"`?

**Answer:**
```python
# mymodule.py
def greet():
    return "Hello"

print(__name__)

if __name__ == "__main__":
    print("Running directly")
else:
    print("Imported as module")

# python mymodule.py     → __name__ = "__main__"  → "Running directly"
# import mymodule        → __name__ = "mymodule"  → "Imported as module"
```

---

## 🔹 Section 9: Generator & Iterator Gotchas

### Q27. 🟡 What is the output?

```python
gen = (x for x in range(3))
print(list(gen))
print(list(gen))
```

**Answer:**
```
[0, 1, 2]
[]
```

**Why?** Generators are **single-use iterators**. After exhaustion, they can't be restarted.

---

### Q28. 🟡 What is the output?

```python
def gen():
    yield 1
    return "done"
    yield 2

g = gen()
print(next(g))
try:
    print(next(g))
except StopIteration as e:
    print(e.value)
```

**Answer:**
```
1
done
```

**Why?** `return` in a generator triggers `StopIteration` with the return value. `yield 2` is never reached.

---

### Q29. 🟡 What is the output?

```python
x = 10
gen = (x for x in range(5))
x = 20
print(list(gen))
```

**Answer:**
```
[0, 1, 2, 3, 4]
```

**Why?** The `x` inside the generator expression is a local variable to the genexp, unrelated to the outer `x`.

**But watch this:**
```python
x = 10
gen = (i + x for i in range(3))
x = 20
print(list(gen))  # [20, 21, 22] — x is looked up lazily!
```

---

## 🔹 Section 10: Decorator & Function Gotchas

### Q30. 🟡 What is the output?

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    """Say hello"""
    return "Hello"

print(greet.__name__)
print(greet.__doc__)
```

**Answer:**
```
wrapper
None
```

**Why?** The decorator replaces `greet` with `wrapper`. The original metadata is lost.

**Fix:**
```python
from functools import wraps

def decorator(func):
    @wraps(func)  # Preserves original name, docstring, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Now greet.__name__ = "greet", greet.__doc__ = "Say hello"
```

---

### Q31. 🟡 What is the output?

```python
funcs = []
for i in range(5):
    def func():
        return i
    funcs.append(func)

print([f() for f in funcs])
```

**Answer:**
```
[4, 4, 4, 4, 4]
```

**Same late-binding closure issue as Q2.** `i` is looked up when called, not when defined.

**Fix:**
```python
funcs = []
for i in range(5):
    def func(i=i):  # Capture current value
        return i
    funcs.append(func)

print([f() for f in funcs])  # [0, 1, 2, 3, 4]
```

---

## 🔹 Section 11: Comparison & Operator Gotchas

### Q32. 🟡 What is the output?

```python
print(True + True + True)
print(True * 10)
print(False * 10)
print(isinstance(True, int))
```

**Answer:**
```
3       ← True = 1, False = 0 (bool is subclass of int)
10
0
True
```

---

### Q33. 🟡 What is the output?

```python
print(1 < 2 < 3)
print(1 < 2 > 0)
print(1 == 1.0 == True)
```

**Answer:**
```
True    ← Chained: (1 < 2) and (2 < 3)
True    ← (1 < 2) and (2 > 0)
True    ← (1 == 1.0) and (1.0 == True)
```

---

### Q34. 🟡 What is the output?

```python
print("" or "hello")
print("world" or "hello")
print("" and "hello")
print("world" and "hello")
print(None or 0 or "" or [] or "found!")
```

**Answer:**
```
hello     ← or returns first truthy, or last value
world     ← "world" is truthy, return it
          ← (empty string) and short-circuits on falsy
hello     ← and returns last truthy if all true
found!    ← or skips all falsy, returns "found!"
```

---

### Q35. 🟡 What is the output?

```python
a = [1, 2, 3]
b = a
c = a[:]

b.append(4)
print(a)
print(c)

print(a == b)
print(a is b)
print(a == c)
print(a is c)
```

**Answer:**
```
[1, 2, 3, 4]    ← b is same object as a
[1, 2, 3]       ← c is a shallow copy

True             ← Same value
True             ← Same object
False            ← Different values now (a has 4)
False            ← Different objects
```

---

## 🔹 Section 12: Python 3.10+ Features (Modern Python)

### Q36. 🟡 What is Structural Pattern Matching (match/case)?

```python
# Python 3.10+
def handle_command(command):
    match command.split():
        case ["quit"]:
            return "Quitting"
        case ["go", direction]:
            return f"Going {direction}"
        case ["get", item] if item != "sword":
            return f"Getting {item}"
        case ["get", "sword"]:
            return "You found the sword!"
        case _:
            return "Unknown command"

print(handle_command("go north"))    # Going north
print(handle_command("get shield"))  # Getting shield
print(handle_command("get sword"))   # You found the sword!
```

---

### Q37. 🟡 What is the walrus operator `:=`?

```python
# Python 3.8+
# Assigns and returns value in one expression

# Without walrus
data = input("Enter: ")
while data != "quit":
    process(data)
    data = input("Enter: ")

# With walrus
while (data := input("Enter: ")) != "quit":
    process(data)

# In list comprehensions
results = [y for x in data if (y := expensive_function(x)) > threshold]

# In if statements
if (n := len(my_list)) > 10:
    print(f"List has {n} elements")
```

---

### Q38. 🟡 What are Exception Groups (Python 3.11+)?

```python
# ExceptionGroup — raise multiple exceptions at once
try:
    raise ExceptionGroup("multiple errors", [
        ValueError("bad value"),
        TypeError("wrong type"),
        KeyError("missing key"),
    ])
except* ValueError as eg:
    print(f"Value errors: {eg.exceptions}")
except* TypeError as eg:
    print(f"Type errors: {eg.exceptions}")

# Output:
# Value errors: (ValueError('bad value'),)
# Type errors: (TypeError('wrong type'),)
# Note: KeyError is re-raised since it wasn't caught
```

---

## 🔹 Section 13: Deep Internals

### Q39. 🔴 How does Python's dict work internally?

**Answer:**
```
Python dict uses a HASH TABLE with open addressing.

1. Key → hash(key) → index in array
2. If collision → probe next slot (linear probing in CPython 3.6+)
3. Since Python 3.7, dicts maintain INSERTION ORDER

Internal structure (CPython):
┌─────────────────────────┐
│  Hash Table (indices)    │  Sparse array of indices
│  [None, 2, None, 0, 1]  │
├─────────────────────────┤
│  Entries (compact array) │  Dense array of [hash, key, value]
│  [hash₀, key₀, val₀]   │
│  [hash₁, key₁, val₁]   │
│  [hash₂, key₂, val₂]   │
└─────────────────────────┘

This split-table design (PEP 412) is why dicts are:
- Memory efficient (compact entries)
- Ordered (entries in insertion order)
- Fast (O(1) average lookup)
```

---

### Q40. 🔴 How does Python's list over-allocate memory?

**Answer:**
```python
import sys

sizes = []
lst = []
for i in range(20):
    lst.append(i)
    sizes.append(sys.getsizeof(lst))
    
print(sizes)
# List grows: 56, 88, 88, 88, 88, 120, 120, 120, 120, 184, ...

# CPython over-allocates to avoid resizing on every append
# Growth pattern: 0, 4, 8, 16, 24, 32, 40, 52, 64, ...
# Formula (roughly): new_size = old_size + (old_size >> 3) + 6
# This gives amortized O(1) appends
```

---

### Q41. 🔴 How does the GIL actually work?

**Answer:**
```
GIL = Global Interpreter Lock (CPython only)

- Only ONE thread can execute Python bytecode at a time
- A thread holds the GIL for ~5ms (sys.getswitchinterval())
- Then it RELEASES the GIL, allowing another thread to run
- I/O operations (file, network) release the GIL

Impact:
- CPU-bound multithreading = NO speedup (limited by GIL)
- I/O-bound multithreading = WORKS (GIL released during I/O)
- multiprocessing = BYPASSES GIL (separate processes)

Python 3.13+ (PEP 703): Experimental "free-threaded" mode
    python3.13t  # No-GIL build
```

---

### Q42. 🔴 What are `__slots__`? When to use them?

```python
# Without __slots__
class Normal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With __slots__
class Optimized:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
n = Normal(1, 2)
o = Optimized(1, 2)

print(sys.getsizeof(n.__dict__))  # 104 bytes (dict overhead)
# Optimized has no __dict__ at all!

print(hasattr(n, '__dict__'))  # True
print(hasattr(o, '__dict__'))  # False

o.z = 3  # AttributeError: 'Optimized' object has no attribute 'z'
# Can't add new attributes — that's the trade-off

# Use __slots__ when:
# - Creating millions of instances
# - Memory is a concern
# - You know all attributes in advance
```

---

## 🔹 Quick Revision — Top 15 Gotchas

| # | Gotcha | Quick Rule |
|---|--------|-----------|
| 1 | Mutable default args | Use `None`, create inside function |
| 2 | Late binding closures | Use `i=i` default arg to capture |
| 3 | `is` vs `==` | `is` = identity, `==` = value |
| 4 | Integer caching | -5 to 256 are cached in CPython |
| 5 | String interning | Only identifier-like strings |
| 6 | `for` loop var leaks | `i` exists after the loop |
| 7 | Tuple with one element | `(1,)` NOT `(1)` |
| 8 | `[[]] * n` trap | Creates n references to SAME list |
| 9 | Dict keys: `True == 1` | `True`, `1`, `1.0` are same key |
| 10 | Float precision | `0.1 + 0.2 != 0.3` |
| 11 | `bool("False") = True` | Any non-empty string is truthy |
| 12 | Generator exhaustion | Single use only |
| 13 | Modify dict during iteration | RuntimeError — iterate over copy |
| 14 | `@wraps` missing | Decorator loses function metadata |
| 15 | `UnboundLocalError` | Assignment anywhere makes var local |

---

*Next: [14_More_Coding_Problems.md](14_More_Coding_Problems.md)*
