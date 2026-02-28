# 02 — Data Structures — Interview Questions

> **45+ questions covering lists, dicts, sets, tuples, collections, time complexity**

---

## 🔹 Section 1: Lists

### Q1. 🟢 What is a list in Python? What are its properties?

**Answer:**
- Ordered, mutable, allows duplicates
- Can hold mixed types
- Dynamically sized (backed by dynamic array)

```python
lst = [1, "hello", 3.14, True, [1, 2]]
lst.append(42)
lst[0] = 99  # Mutable
```

**Time complexities:**
| Operation | Complexity |
|-----------|-----------|
| `append()` | O(1) amortized |
| `pop()` (last) | O(1) |
| `pop(i)` | O(n) |
| `insert(i, x)` | O(n) |
| `remove(x)` | O(n) |
| `x in lst` | O(n) |
| `lst[i]` | O(1) |
| `sort()` | O(n log n) |

---

### Q2. 🟡 How is a Python list implemented internally?

**Answer:**
Python list is a **dynamic array** (not a linked list).

- Stores an array of **pointers** to objects
- Over-allocates memory to avoid resizing on every append
- When capacity is exceeded, allocates ~1.125x the current size

```python
import sys
lst = []
for i in range(20):
    lst.append(i)
    print(f"len={len(lst)}, size={sys.getsizeof(lst)} bytes")
# Size jumps: 56 → 88 → 120 → 184 → 248...
```

**Why it matters:** `append()` is O(1) amortized, but `insert(0, x)` is O(n) because all elements shift.

---

### Q3. 🟡 What are the different ways to copy a list?

**Answer:**
```python
original = [1, [2, 3], 4]

# 1. Assignment (NOT a copy — same reference)
a = original
a[0] = 99
print(original)  # [99, [2, 3], 4] ← Changed!

# 2. Shallow copy methods (all equivalent)
b = original.copy()
c = original[:]
d = list(original)

# 3. Deep copy
import copy
e = copy.deepcopy(original)
e[1].append(99)
print(original)  # [1, [2, 3], 4] ← NOT changed
```

---

### Q4. 🟢 What is list slicing? Explain with examples.

**Answer:**
```python
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

lst[2:5]      # [2, 3, 4]       — start:stop
lst[:3]       # [0, 1, 2]       — first 3
lst[7:]       # [7, 8, 9]       — from index 7
lst[-3:]      # [7, 8, 9]       — last 3
lst[::2]      # [0, 2, 4, 6, 8] — every 2nd
lst[::-1]     # [9, 8, 7, ...]  — reverse
lst[1:8:2]    # [1, 3, 5, 7]    — start:stop:step

# Slicing creates a NEW list (shallow copy)
new = lst[2:5]
new[0] = 99
print(lst[2])  # 2 (unchanged — for immutable elements)
```

---

### Q5. 🟡 How do you sort a list? `sort()` vs `sorted()`?

**Answer:**
```python
lst = [3, 1, 4, 1, 5, 9]

# sort() — in-place, returns None
lst.sort()
print(lst)  # [1, 1, 3, 4, 5, 9]

# sorted() — returns NEW list, original unchanged
lst = [3, 1, 4, 1, 5, 9]
new = sorted(lst)
print(lst)  # [3, 1, 4, 1, 5, 9] (unchanged)
print(new)  # [1, 1, 3, 4, 5, 9]

# Custom sorting
users = [("Sid", 25), ("Raj", 30), ("Amit", 22)]
users.sort(key=lambda u: u[1])  # Sort by age
# [('Amit', 22), ('Sid', 25), ('Raj', 30)]

# Reverse
sorted(lst, reverse=True)
```

| Feature | `sort()` | `sorted()` |
|---------|----------|------------|
| Returns | `None` | New list |
| Modifies original | Yes | No |
| Works on | Lists only | Any iterable |
| Algorithm | Timsort | Timsort |

---

## 🔹 Section 2: Dictionaries

### Q6. 🟢 What is a dictionary? What are its properties?

**Answer:**
- Key-value pairs, **ordered** (Python 3.7+ insertion order guaranteed)
- Keys must be **hashable** (immutable: str, int, tuple)
- Values can be anything
- O(1) average lookup, insert, delete

```python
user = {
    "name": "Sid",
    "age": 25,
    "skills": ["Python", "Django"]
}

user["name"]           # "Sid"
user.get("email", "N/A")  # "N/A" (default if missing)
```

---

### Q7. 🟡 How are dictionaries implemented internally?

**Answer:**
Python dict uses a **hash table** (open addressing).

```
key → hash(key) → index in array → (hash, key, value)
```

**Steps:**
1. Compute hash of key: `hash(key)`
2. Map hash to index: `hash % table_size`
3. If collision → probe next slot (open addressing)

**Python 3.6+:** Uses compact dict — separate arrays for hash indices and key-value pairs → less memory, preserves insertion order.

**Important:** Keys must be hashable:
```python
# ✅ Hashable (immutable)
d = {1: "a", "key": "b", (1, 2): "c"}

# ❌ Not hashable (mutable)
d = {[1, 2]: "a"}    # TypeError: unhashable type: 'list'
d = {{1: 2}: "a"}    # TypeError: unhashable type: 'dict'
```

---

### Q8. 🟡 What is the difference between `dict[key]` and `dict.get(key)`?

**Answer:**
```python
d = {"name": "Sid"}

# dict[key] — raises KeyError if missing
d["age"]           # KeyError: 'age'

# dict.get(key) — returns None (or default) if missing
d.get("age")       # None
d.get("age", 25)   # 25 (custom default)
```

**Backend tip:** Always use `.get()` for optional fields from API requests:
```python
page = request.args.get("page", 1)     # Flask
limit = request.query_params.get("limit", 10)  # DRF
```

---

### Q9. 🟡 What are `defaultdict`, `OrderedDict`, and `Counter`?

**Answer:**
```python
from collections import defaultdict, OrderedDict, Counter

# defaultdict — auto-creates default values
word_count = defaultdict(int)
for word in ["a", "b", "a", "c", "a"]:
    word_count[word] += 1
# {'a': 3, 'b': 1, 'c': 1}

group = defaultdict(list)
for name, dept in [("Sid", "eng"), ("Raj", "eng"), ("Amit", "sales")]:
    group[dept].append(name)
# {'eng': ['Sid', 'Raj'], 'sales': ['Amit']}

# Counter — count elements
c = Counter("aabbbcccc")
print(c)                    # Counter({'c': 4, 'b': 3, 'a': 2})
print(c.most_common(2))     # [('c', 4), ('b', 3)]

# OrderedDict — preserves insertion order (all dicts do since 3.7)
# Still useful for: move_to_end(), equality checks consider order
od = OrderedDict()
od["a"] = 1
od["b"] = 2
od.move_to_end("a")  # Move to end
```

---

### Q10. 🟡 How do you merge two dictionaries?

**Answer:**
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

# Method 1: | operator (Python 3.9+) — BEST
merged = d1 | d2         # {'a': 1, 'b': 3, 'c': 4}

# Method 2: |= in-place update (Python 3.9+)
d1 |= d2

# Method 3: ** unpacking (Python 3.5+)
merged = {**d1, **d2}

# Method 4: update()
d1.update(d2)             # Modifies d1 in-place

# Method 5: ChainMap (doesn't merge, layers)
from collections import ChainMap
chain = ChainMap(d2, d1)  # d2 takes priority
```

**Note:** In all cases, the RIGHTMOST dict's values win on conflicts.

---

### Q11. 🟡 What is a `dict comprehension`? Give practical examples.

**Answer:**
```python
# Basic
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# With condition
even_sq = {x: x**2 for x in range(10) if x % 2 == 0}

# Swap keys and values
original = {"a": 1, "b": 2}
swapped = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b'}

# From two lists
keys = ["name", "age", "city"]
values = ["Sid", 25, "Bangalore"]
d = dict(zip(keys, values))
# OR
d = {k: v for k, v in zip(keys, values)}
```

---

## 🔹 Section 3: Sets

### Q12. 🟢 What is a set? When should you use it?

**Answer:**
- Unordered, mutable, **no duplicates**
- Elements must be hashable
- O(1) average for add, remove, lookup

```python
s = {1, 2, 3, 3, 3}
print(s)  # {1, 2, 3}

# Use sets when:
# 1. Remove duplicates
unique = list(set([1, 2, 2, 3, 3]))

# 2. Fast membership testing
valid_statuses = {"active", "pending", "closed"}
if user_status in valid_statuses:  # O(1) vs O(n) for list
    pass

# 3. Set operations (intersection, union, etc.)
```

---

### Q13. 🟡 What are the set operations?

**Answer:**
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union — all elements from both
a | b                  # {1, 2, 3, 4, 5, 6}
a.union(b)

# Intersection — common elements
a & b                  # {3, 4}
a.intersection(b)

# Difference — in a but not b
a - b                  # {1, 2}
a.difference(b)

# Symmetric difference — in a or b but not both
a ^ b                  # {1, 2, 5, 6}
a.symmetric_difference(b)

# Subset / Superset
{1, 2} <= {1, 2, 3}   # True (subset)
{1, 2, 3} >= {1, 2}   # True (superset)
```

**Backend use:** Finding common tags, permissions checking, deduplication.

---

### Q14. 🟡 What is `frozenset`?

**Answer:**
An **immutable** set — can be used as a dict key or inside another set.

```python
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError: no 'add' method

# Use as dict key
cache = {
    frozenset(["admin", "user"]): "full_access",
    frozenset(["user"]): "limited_access"
}

# Use inside another set
set_of_sets = {frozenset([1, 2]), frozenset([3, 4])}
```

---

## 🔹 Section 4: Tuples

### Q15. 🟢 What is a tuple? When should you use it?

**Answer:**
- Ordered, **immutable**, allows duplicates
- Faster and uses less memory than lists
- Hashable (if elements are hashable)

```python
t = (1, 2, 3)
# t[0] = 99  # TypeError: no item assignment

# Single element tuple (need trailing comma!)
single = (42,)     # ✅ tuple
not_tuple = (42)   # ❌ just an int

# Tuple unpacking
name, age, city = ("Sid", 25, "Bangalore")
a, *rest, b = (1, 2, 3, 4, 5)  # a=1, rest=[2,3,4], b=5
```

**Use tuples for:**
- Function return values: `return (status, data, error)`
- Dict keys: `cache[(user_id, date)] = result`
- Named constants: `RGB = (255, 128, 0)`
- Immutable records

---

### Q16. 🟡 What is `namedtuple`? How is it better than a regular tuple?

**Answer:**
```python
from collections import namedtuple

# Regular tuple — what does each index mean?
user = ("Sid", 25, "Bangalore")
print(user[0])  # "Sid" — not clear

# Named tuple — self-documenting
User = namedtuple("User", ["name", "age", "city"])
user = User(name="Sid", age=25, city="Bangalore")
print(user.name)   # "Sid" ✅ clear!
print(user[0])     # "Sid" still works
print(user._asdict())  # {'name': 'Sid', 'age': 25, 'city': 'Bangalore'}

# Immutable like tuple
# user.name = "Raj"  # AttributeError
```

**Modern alternative:** `dataclass` (Python 3.7+) — more features, mutable by default.

---

## 🔹 Section 5: Strings

### Q17. 🟢 Are strings mutable or immutable?

**Answer:**
**Immutable.** Every string operation creates a new string.

```python
s = "hello"
# s[0] = "H"  # TypeError

# This creates a NEW string
s = s.upper()  # "HELLO" (new object)

# String concatenation in loop is BAD
# ❌ O(n²) — creates new string each time
result = ""
for word in words:
    result += word

# ✅ O(n) — join is optimized
result = "".join(words)
```

---

### Q18. 🟡 What are the most important string methods for backend?

**Answer:**
```python
s = "  Hello, World!  "

# Cleaning
s.strip()           # "Hello, World!" — remove whitespace
s.lstrip()          # "Hello, World!  "
s.rstrip()          # "  Hello, World!"

# Searching
s.find("World")     # 9 (index, -1 if not found)
s.index("World")    # 9 (index, ValueError if not found)
s.count("l")        # 3
s.startswith("  He") # True
s.endswith("!  ")    # True

# Transforming
s.lower()           # "  hello, world!  "
s.upper()           # "  HELLO, WORLD!  "
s.title()           # "  Hello, World!  "
s.replace("World", "Python")

# Splitting/Joining
"a,b,c".split(",")          # ['a', 'b', 'c']
",".join(["a", "b", "c"])   # "a,b,c"

# Validation
"abc123".isalnum()   # True
"abc".isalpha()      # True
"123".isdigit()      # True

# Backend essential: URL/path manipulation
"/api/users/123/".strip("/").split("/")  # ['api', 'users', '123']
```

---

## 🔹 Section 6: Advanced Data Structures

### Q19. 🟡 What is `deque`? When to use it over a list?

**Answer:**
```python
from collections import deque

# deque — double-ended queue
dq = deque([1, 2, 3])
dq.appendleft(0)    # O(1) — list.insert(0, x) is O(n)!
dq.popleft()         # O(1) — list.pop(0) is O(n)!
dq.append(4)         # O(1)
dq.pop()             # O(1)

# Fixed-size deque (sliding window)
recent = deque(maxlen=5)
for i in range(10):
    recent.append(i)
print(recent)  # deque([5, 6, 7, 8, 9])
```

| Operation | List | Deque |
|-----------|------|-------|
| `append()` | O(1) | O(1) |
| `pop()` | O(1) | O(1) |
| `insert(0, x)` | O(n) | O(1) |
| `pop(0)` | O(n) | O(1) |
| `access [i]` | O(1) | O(n) |

**Use deque for:** Queues, BFS, sliding windows, recent history.

---

### Q20. 🟡 What is `heapq`? How to implement a priority queue?

**Answer:**
```python
import heapq

# Min-heap
nums = [5, 3, 8, 1, 9]
heapq.heapify(nums)        # In-place, O(n)
print(nums)                 # [1, 3, 8, 5, 9]

heapq.heappush(nums, 2)    # Add element
smallest = heapq.heappop(nums)  # Remove & return smallest (1)

# Top K elements
heapq.nlargest(3, nums)    # [9, 8, 5]
heapq.nsmallest(3, nums)   # [2, 3, 5]

# Max-heap trick (negate values)
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
largest = -heapq.heappop(max_heap)  # 5

# Priority Queue with tuples
tasks = []
heapq.heappush(tasks, (1, "High priority"))
heapq.heappush(tasks, (3, "Low priority"))
heapq.heappush(tasks, (2, "Medium priority"))
print(heapq.heappop(tasks))  # (1, 'High priority')
```

---

### Q21. 🟡 What is `bisect`? Binary search in sorted list.

**Answer:**
```python
import bisect

sorted_list = [10, 20, 30, 40, 50]

# Find insertion point
bisect.bisect_left(sorted_list, 25)   # 2
bisect.bisect_right(sorted_list, 30)  # 3

# Insert while maintaining sort
bisect.insort(sorted_list, 25)  # [10, 20, 25, 30, 40, 50]
```

---

### Q22. 🟡 What is `ChainMap`?

**Answer:**
```python
from collections import ChainMap

defaults = {"color": "red", "size": "medium"}
user_prefs = {"color": "blue"}
env_vars = {"size": "large", "debug": True}

# ChainMap — searches in order, first match wins
config = ChainMap(env_vars, user_prefs, defaults)
print(config["color"])   # "blue" (from user_prefs)
print(config["size"])    # "large" (from env_vars)
print(config["debug"])   # True
```

**Backend use:** Layered configuration (env vars > user config > defaults).

---

## 🔹 Section 7: Time & Space Complexity

### Q23. 🟡 What is the time complexity of common operations?

**Answer:**

| Data Structure | Operation | Average | Worst |
|---------------|-----------|---------|-------|
| **List** | Index `[i]` | O(1) | O(1) |
| **List** | Search `in` | O(n) | O(n) |
| **List** | Append | O(1)* | O(n) |
| **List** | Insert/Delete at i | O(n) | O(n) |
| **Dict** | Get/Set/Delete | O(1) | O(n) |
| **Dict** | Search `in` | O(1) | O(n) |
| **Set** | Add/Remove/Search | O(1) | O(n) |
| **Deque** | Append/Pop (both ends) | O(1) | O(1) |
| **Heap** | Push/Pop | O(log n) | O(log n) |
| **Heap** | Heapify | O(n) | O(n) |

*Amortized

---

### Q24. 🟢 When should you use which data structure?

**Answer:**

| Need | Use |
|------|-----|
| Ordered collection, frequent append/pop | `list` |
| Fast lookup by key | `dict` |
| Unique elements, fast membership | `set` |
| Immutable sequence | `tuple` |
| Queue or deque operations | `deque` |
| Priority queue | `heapq` |
| Count elements | `Counter` |
| Default values for missing keys | `defaultdict` |
| Bidirectional mapping | Two dicts |
| Graph adjacency list | `defaultdict(list)` |
| LRU Cache | `OrderedDict` or `functools.lru_cache` |

---

## 🔹 Section 8: Tricky Output Questions

### Q25. 🟡 What is the output?

```python
lst = [1, 2, 3]
lst2 = lst * 2
print(lst2)
```

**Answer:** `[1, 2, 3, 1, 2, 3]` — repeats elements.

---

### Q26. 🟡 What is the output?

```python
lst = [[]] * 3
lst[0].append(1)
print(lst)
```

**Answer:** `[[1], [1], [1]]`

Because `[[]] * 3` creates 3 references to the SAME inner list.

Fix:
```python
lst = [[] for _ in range(3)]
lst[0].append(1)
print(lst)  # [[1], [], []]
```

---

### Q27. 🟡 What is the output?

```python
d = {}
d[True] = "yes"
d[1] = "one"
d[1.0] = "float_one"
print(d)
```

**Answer:** `{True: 'float_one'}`

Because `True == 1 == 1.0` and `hash(True) == hash(1) == hash(1.0)`. They're considered the same key.

---

### Q28. 🟡 What is the output?

```python
t = (1, 2, [3, 4])
t[2].append(5)
print(t)
```

**Answer:** `(1, 2, [3, 4, 5])`

The tuple is immutable, but the list INSIDE it is mutable. You can't reassign `t[2]`, but you can modify the list object it points to.

---

### Q29. 🟡 What is the output?

```python
a = {1, 2, 3}
b = {3, 4, 5}
print(a - b)
print(b - a)
```

**Answer:**
```
{1, 2}
{4, 5}
```
Set difference is NOT commutative.

---

### Q30. 🟡 How do you reverse a dictionary?

**Answer:**
```python
original = {"a": 1, "b": 2, "c": 3}

# Method 1: Dict comprehension
reversed_d = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Method 2: zip
reversed_d = dict(zip(original.values(), original.keys()))

# ⚠️ Warning: If values aren't unique, later ones overwrite
d = {"a": 1, "b": 1}
reversed_d = {v: k for k, v in d.items()}  # {1: 'b'} — 'a' lost!
```

---

## 🔹 Section 9: Practical Backend Questions

### Q31. 🟡 How would you count word frequency in a text?

**Answer:**
```python
from collections import Counter

text = "the quick brown fox jumps over the lazy dog the fox"

# Method 1: Counter (best)
word_count = Counter(text.split())
print(word_count.most_common(3))
# [('the', 3), ('fox', 2), ('quick', 1)]

# Method 2: defaultdict
from collections import defaultdict
freq = defaultdict(int)
for word in text.split():
    freq[word] += 1

# Method 3: dict.get()
freq = {}
for word in text.split():
    freq[word] = freq.get(word, 0) + 1
```

---

### Q32. 🟡 How do you find duplicates in a list?

**Answer:**
```python
lst = [1, 2, 3, 2, 4, 3, 5]

# Method 1: Counter
from collections import Counter
dupes = [item for item, count in Counter(lst).items() if count > 1]
# [2, 3]

# Method 2: Set tracking
seen = set()
dupes = set()
for item in lst:
    if item in seen:
        dupes.add(item)
    seen.add(item)

# Method 3: One-liner (less efficient)
dupes = set(x for x in lst if lst.count(x) > 1)
```

---

### Q33. 🟡 How would you flatten a nested list?

**Answer:**
```python
nested = [[1, 2], [3, 4], [5, 6]]

# Method 1: List comprehension (1 level)
flat = [x for sublist in nested for x in sublist]
# [1, 2, 3, 4, 5, 6]

# Method 2: itertools.chain
from itertools import chain
flat = list(chain.from_iterable(nested))

# Method 3: Deep flatten (recursive)
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

deep = [1, [2, [3, [4]], 5]]
print(flatten(deep))  # [1, 2, 3, 4, 5]
```

---

### Q34. 🟡 How do you implement an LRU Cache?

**Answer:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest

# Or use functools (simpler)
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    return n * n
```

---

### Q35. 🟡 How do you group a list of dicts by a key?

**Answer:**
```python
from collections import defaultdict
from itertools import groupby

users = [
    {"name": "Sid", "dept": "eng"},
    {"name": "Raj", "dept": "eng"},
    {"name": "Amit", "dept": "sales"},
    {"name": "Neha", "dept": "sales"},
]

# Method 1: defaultdict
groups = defaultdict(list)
for user in users:
    groups[user["dept"]].append(user["name"])
# {'eng': ['Sid', 'Raj'], 'sales': ['Amit', 'Neha']}

# Method 2: itertools.groupby (requires sorted input!)
users_sorted = sorted(users, key=lambda u: u["dept"])
for dept, group in groupby(users_sorted, key=lambda u: u["dept"]):
    print(dept, [u["name"] for u in group])
```

---

### Q36. 🟡 Difference between `array` module and `list`?

**Answer:**
```python
from array import array

# array — typed, memory efficient (stores raw values)
arr = array('i', [1, 2, 3, 4])  # 'i' = signed int

# list — stores pointers to objects (more memory)
lst = [1, 2, 3, 4]
```

| Feature | `list` | `array` | `numpy.array` |
|---------|--------|---------|----------------|
| Types | Mixed | Single type | Single type |
| Memory | More | Less | Least |
| Speed | Slower | Faster | Fastest |
| Features | Most | Basic | Math operations |
| Use case | General | I/O, ctypes | Data science |

---

### Q37. 🟡 What is the difference between `queue.Queue` and `collections.deque`?

**Answer:**

| Feature | `Queue` | `deque` |
|---------|---------|---------|
| Thread-safe | ✅ Yes (has locks) | ❌ No |
| Blocking | ✅ `get(block=True)` | ❌ No |
| Timeout | ✅ `get(timeout=5)` | ❌ No |
| Performance | Slower (locks) | Faster |
| Use case | Multi-threaded | Single-threaded |

```python
# For multi-threaded producer-consumer
from queue import Queue
q = Queue(maxsize=100)
q.put(item)          # Blocks if full
item = q.get()       # Blocks if empty

# For single-threaded
from collections import deque
dq = deque()
dq.append(item)
item = dq.popleft()
```

---

## 🔹 Section 10: Data Structure Selection Questions

### Q38. 🟡 Design a data structure for...

**Q: Store user sessions with fast lookup and expiry?**
```python
# Dict with TTL — or use Redis in production
sessions = {}  # {session_id: {"user_id": 1, "expires": datetime}}

# Production: Redis with TTL
# redis.setex(session_id, ttl_seconds, user_data)
```

**Q: Count API endpoint hits in last 5 minutes?**
```python
from collections import deque
from time import time

class RateLimiter:
    def __init__(self, window=300):
        self.requests = deque()
        self.window = window
    
    def hit(self):
        now = time()
        self.requests.append(now)
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()
    
    def count(self):
        return len(self.requests)
```

**Q: Implement auto-complete suggestions?**
```python
# Trie (prefix tree)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
```

---

### Q39. 🟡 How would you implement a stack and queue using Python?

**Answer:**
```python
# Stack — LIFO (Last In, First Out)
stack = []
stack.append(1)     # push
stack.append(2)
top = stack.pop()   # pop → 2

# Queue — FIFO (First In, First Out)
from collections import deque
queue = deque()
queue.append(1)     # enqueue
queue.append(2)
first = queue.popleft()  # dequeue → 1

# ❌ Don't use list for queue
# list.pop(0) is O(n)!
```

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | List vs Tuple? | Mutable vs Immutable |
| 2 | Dict lookup time? | O(1) average |
| 3 | How to remove duplicates? | `list(set(lst))` |
| 4 | `list.sort()` vs `sorted()`? | In-place vs new list |
| 5 | Dict keys requirements? | Must be hashable (immutable) |
| 6 | `defaultdict` purpose? | Auto-create default values |
| 7 | Best for queue? | `collections.deque` |
| 8 | `[[]] * 3` trap? | All three share same inner list |
| 9 | `Counter` use? | Count element frequencies |
| 10 | List internal impl? | Dynamic array of pointers |

---

*Next: [03_OOP.md](03_OOP.md)*
