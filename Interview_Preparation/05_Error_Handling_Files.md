# 05 — Error Handling & File I/O — Interview Questions

> **30+ questions covering exceptions, context managers, file operations, logging**

---

## 🔹 Section 1: Exception Handling

### Q1. 🟢 What is exception handling? Why is it important?

**Answer:**
Exception handling allows you to gracefully manage runtime errors instead of crashing.

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")      # Handle the error
else:
    print("Success")           # Runs if NO exception
finally:
    print("Always runs")       # Cleanup — runs ALWAYS
```

**Backend importance:**
- API shouldn't crash on bad user input
- Database connections must be closed on error
- Graceful error responses (500, 400, 404)
- Logging errors for debugging

---

### Q2. 🟢 What is the exception hierarchy?

**Answer:**
```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    ├── AttributeError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── FileNotFoundError
    ├── PermissionError
    ├── OSError
    │   └── ConnectionError
    │       ├── ConnectionRefusedError
    │       └── ConnectionResetError
    ├── RuntimeError
    │   └── RecursionError
    └── StopIteration
```

**Rule:** Always catch `Exception`, never `BaseException` (would catch SystemExit/KeyboardInterrupt).

---

### Q3. 🟡 What is the order of `except` blocks? Does it matter?

**Answer:**
Yes! Python checks `except` blocks top to bottom. Put specific exceptions first.

```python
# ❌ Wrong — generic catches everything
try:
    d = {}
    d["key"]
except Exception:
    print("Generic")
except KeyError:
    print("Key error")  # NEVER reached!

# ✅ Correct — specific first
try:
    d = {}
    d["key"]
except KeyError:
    print("Key error")   # Caught here ✅
except Exception:
    print("Generic")     # Catches everything else
```

---

### Q4. 🟡 How do you create a custom exception?

**Answer:**
```python
# Simple
class InsufficientFundsError(Exception):
    pass

# With custom attributes
class APIError(Exception):
    def __init__(self, message, status_code, endpoint):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint = endpoint
    
    def __str__(self):
        return f"[{self.status_code}] {self.endpoint}: {self.args[0]}"

# Usage
try:
    raise APIError("Not found", 404, "/api/users/999")
except APIError as e:
    print(e)              # [404] /api/users/999: Not found
    print(e.status_code)  # 404

# Backend pattern: Exception hierarchy
class AppError(Exception): pass
class ValidationError(AppError): pass
class AuthenticationError(AppError): pass
class NotFoundError(AppError): pass
```

---

### Q5. 🟡 What is the difference between `raise` and `raise from`?

**Answer:**
```python
# raise — re-raises or raises new exception
try:
    int("abc")
except ValueError:
    raise RuntimeError("Conversion failed")
    # Original ValueError is still visible in traceback

# raise from — explicit exception chaining
try:
    int("abc")
except ValueError as e:
    raise RuntimeError("Conversion failed") from e
    # Shows: "The above exception was the direct cause of..."

# raise from None — suppress original exception
try:
    int("abc")
except ValueError:
    raise RuntimeError("Invalid input") from None
    # Original ValueError is hidden
```

---

### Q6. 🟡 What is `else` in try/except?

**Answer:**
```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division error")
else:
    # Runs ONLY if no exception occurred
    print(f"Result: {result}")
finally:
    # Runs ALWAYS
    print("Done")
```

**Why use `else`?** Keeps the `try` block minimal — only the code that might raise goes in `try`.

```python
# ✅ Good — minimal try block
try:
    data = json.loads(raw_json)
except json.JSONDecodeError:
    return {"error": "Invalid JSON"}, 400
else:
    process(data)
    save_to_db(data)
```

---

### Q7. 🟡 What exceptions should you catch in a REST API?

**Answer:**
```python
# Flask example
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error="Bad request"), 400

@app.errorhandler(500)
def server_error(e):
    # Log the actual error
    app.logger.error(f"Server error: {e}")
    return jsonify(error="Internal server error"), 500

# In route handlers:
@app.route("/users/<int:user_id>")
def get_user(user_id):
    try:
        user = db.get_user(user_id)
    except NotFoundError:
        return jsonify(error="User not found"), 404
    except DatabaseError as e:
        app.logger.error(f"DB error: {e}")
        return jsonify(error="Service unavailable"), 503
    else:
        return jsonify(user.to_dict()), 200
```

---

### Q8. 🟡 What is EAFP vs LBYL?

**Answer:**

**EAFP** = Easier to Ask Forgiveness than Permission (Pythonic)
**LBYL** = Look Before You Leap (Non-Pythonic)

```python
# LBYL — Check before acting
if "key" in my_dict:
    value = my_dict["key"]
else:
    value = "default"

# EAFP — Try and handle exception (Pythonic ✅)
try:
    value = my_dict["key"]
except KeyError:
    value = "default"

# Even better:
value = my_dict.get("key", "default")
```

**Why EAFP is preferred:**
- Race conditions: File might be deleted between check and read
- More concise
- Faster when exception is rare (happy path optimization)

---

## 🔹 Section 2: File Handling

### Q9. 🟢 How do you read/write files in Python?

**Answer:**
```python
# Always use 'with' (context manager) — auto-closes file
# Reading
with open("file.txt", "r") as f:
    content = f.read()          # Entire file as string
    # OR
    lines = f.readlines()       # List of lines
    # OR
    for line in f:              # Line by line (memory efficient)
        process(line)

# Writing
with open("file.txt", "w") as f:    # Overwrites
    f.write("Hello\n")

with open("file.txt", "a") as f:    # Appends
    f.write("World\n")

# Read + Write
with open("file.txt", "r+") as f:
    content = f.read()
    f.write("appended")
```

**File modes:**
| Mode | Description |
|------|-------------|
| `r` | Read (default) |
| `w` | Write (overwrites) |
| `a` | Append |
| `r+` | Read + Write |
| `rb` / `wb` | Binary mode |
| `x` | Exclusive create (error if exists) |

---

### Q10. 🟡 How do you read a large file efficiently?

**Answer:**
```python
# ❌ Bad — loads entire file into memory
with open("huge.log") as f:
    data = f.read()  # 10GB file = 10GB in RAM!

# ✅ Good — line by line (generator-like)
with open("huge.log") as f:
    for line in f:  # File object is an iterator
        process(line)

# ✅ Good — chunked reading
def read_in_chunks(file_path, chunk_size=8192):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# ✅ Good — generator function
def search_logs(file_path, keyword):
    with open(file_path) as f:
        for line_num, line in enumerate(f, 1):
            if keyword in line:
                yield line_num, line.strip()

for num, line in search_logs("server.log", "ERROR"):
    print(f"Line {num}: {line}")
```

---

### Q11. 🟡 How do you work with JSON files?

**Answer:**
```python
import json

# Write JSON
data = {"name": "Sid", "age": 25, "skills": ["Python", "Django"]}
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)  # Pretty print

# Read JSON
with open("data.json", "r") as f:
    data = json.load(f)

# String conversion
json_str = json.dumps(data)              # Dict → JSON string
data = json.loads('{"name": "Sid"}')     # JSON string → Dict

# Custom serialization
from datetime import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps({"created": datetime.now()}, cls=DateEncoder)
```

---

### Q12. 🟡 How do you work with CSV files?

**Answer:**
```python
import csv

# Write CSV
with open("users.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age", "city"])  # Header
    writer.writerow(["Sid", 25, "Bangalore"])
    writer.writerows([
        ["Raj", 30, "Mumbai"],
        ["Amit", 28, "Delhi"]
    ])

# Read CSV
with open("users.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print(row)  # ['Sid', '25', 'Bangalore']

# DictReader/DictWriter (more readable)
with open("users.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

---

### Q13. 🟡 What is the `pathlib` module? Why use it over `os.path`?

**Answer:**
```python
from pathlib import Path

# Create path objects
home = Path.home()
project = Path("/Users/sid/project")
file = project / "src" / "main.py"  # / operator for joining!

# Common operations
file.exists()          # True/False
file.is_file()         # True/False
file.is_dir()          # True/False
file.name              # "main.py"
file.stem              # "main"
file.suffix            # ".py"
file.parent            # Path('/Users/sid/project/src')

# Read/Write (Python 3.5+)
content = file.read_text()
file.write_text("Hello")

# Glob
for py_file in project.glob("**/*.py"):
    print(py_file)

# Create directories
Path("new/nested/dir").mkdir(parents=True, exist_ok=True)
```

| Feature | `os.path` | `pathlib` |
|---------|-----------|-----------|
| Style | Functions | OOP |
| Joining | `os.path.join(a, b)` | `a / b` |
| Modern | Old | Python 3.4+ |
| Readability | Less | More ✅ |

---

## 🔹 Section 3: Logging

### Q14. 🟡 How do you set up logging in Python?

**Answer:**
```python
import logging

# Basic setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)

logger.debug("Debug info")      # Not shown (level is INFO)
logger.info("Server started")   # Shown
logger.warning("Disk 90% full") # Shown
logger.error("DB connection failed")  # Shown
logger.critical("System crash!")       # Shown
```

**Levels (low to high):**
| Level | Value | Use Case |
|-------|-------|----------|
| DEBUG | 10 | Development details |
| INFO | 20 | General operations |
| WARNING | 30 | Something unexpected |
| ERROR | 40 | Operation failed |
| CRITICAL | 50 | System failure |

---

### Q15. 🟡 What is structured logging? Why use it in backend?

**Answer:**
```python
import logging
import json

# Structured logging — machine-parseable
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

# Production setup
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("myapp")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User login", extra={"user_id": 123})
# {"timestamp": "2026-02-28", "level": "INFO", "message": "User login", ...}
```

**Why structured logging:**
- Easily parsed by ELK Stack, Datadog, Splunk
- Searchable and filterable
- Better for production monitoring

---

## 🔹 Section 4: Tricky Questions

### Q16. 🟡 What is the output?

```python
try:
    try:
        raise ValueError("inner")
    except ValueError:
        print("caught inner")
        raise TypeError("converted")
except TypeError:
    print("caught outer")
finally:
    print("final")
```

**Answer:**
```
caught inner
caught outer
final
```

---

### Q17. 🟡 What is the output?

```python
def func():
    try:
        return "try"
    finally:
        return "finally"

print(func())
```

**Answer:** `finally` — The `finally` block's return overrides the `try` block's return.

**Rule:** Never put `return` in `finally` — it swallows exceptions and overrides returns.

---

### Q18. 🟡 What is the output?

```python
try:
    raise ValueError("error")
except ValueError as e:
    print(type(e))
    print(e.args)
```

**Answer:**
```
<class 'ValueError'>
('error',)
```

---

### Q19. 🟡 Can you catch multiple exceptions in one block?

**Answer:**
```python
# Multiple exceptions in one block
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print(f"Error: {e}")

# Different handling for different exceptions
try:
    data = fetch_data()
except ConnectionError:
    retry()
except TimeoutError:
    use_cache()
except Exception as e:
    log_error(e)
    raise
```

---

### Q20. 🟡 What is `assert`? When to use it?

**Answer:**
```python
# assert expression, "error message"
assert 2 + 2 == 4, "Math is broken"
assert isinstance(data, dict), f"Expected dict, got {type(data)}"

# Removed with -O flag!
# python -O script.py → all asserts are skipped

# ✅ Use for:
assert len(items) > 0  # Development/debugging checks
assert user.is_admin   # Internal invariants

# ❌ Never use for:
# Input validation (user can bypass with -O)
# Security checks
# Production error handling
```

---

## 🔹 Section 5: Practical Backend Patterns

### Q21. 🟡 Write a global exception handler for a Flask API.

**Answer:**
```python
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

class AppException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

@app.errorhandler(AppException)
def handle_app_error(error):
    return jsonify({"error": str(error)}), error.status_code

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(Exception)
def handle_unexpected(error):
    logger.exception("Unexpected error")
    return jsonify({"error": "Internal server error"}), 500
```

---

### Q22. 🟡 How do you handle database connection errors?

**Answer:**
```python
import time
from contextlib import contextmanager

@contextmanager
def get_db_connection(max_retries=3, delay=1):
    conn = None
    for attempt in range(max_retries):
        try:
            conn = create_connection()
            yield conn
            conn.commit()
            return
        except ConnectionError as e:
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                raise
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
```

---

### Q23. 🟡 What is `warnings` module?

**Answer:**
```python
import warnings

# Issue a warning (doesn't stop execution)
warnings.warn("This function is deprecated", DeprecationWarning)

# Control warning behavior
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("error", category=FutureWarning)  # Treat as exception

# Custom warning
class PerformanceWarning(UserWarning):
    pass

if query_time > 5:
    warnings.warn(f"Slow query: {query_time}s", PerformanceWarning)
```

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | `try/except/else/finally` order? | try → except (if error) → else (if no error) → finally (always) |
| 2 | Catch `Exception` or `BaseException`? | `Exception` — never `BaseException` |
| 3 | EAFP vs LBYL? | EAFP = try/except (Pythonic), LBYL = check first |
| 4 | `raise from` purpose? | Explicit exception chaining |
| 5 | Read large file? | `for line in f:` (iterator) |
| 6 | `json.dump` vs `json.dumps`? | File vs String |
| 7 | `os.path` vs `pathlib`? | Old functions vs Modern OOP |
| 8 | `assert` in production? | No — removed with `-O` flag |
| 9 | Logging levels? | DEBUG < INFO < WARNING < ERROR < CRITICAL |
| 10 | `with` statement purpose? | Auto cleanup (close files, connections) |

---

*Next: [06_Advanced_Python.md](06_Advanced_Python.md)*
