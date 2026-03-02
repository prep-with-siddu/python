"""
=============================================================================
 FUNCTIONS — HANDS-ON INTERVIEW EXERCISES (3 Years Experience Level)
=============================================================================
 Covers: 3.1 Function Basics + 3.2 Advanced Functions (100% checklist)
 
 Topics:
   - Keyword/Positional args, *args, **kwargs, docstrings
   - First-class functions, higher-order functions, lambda
   - map(), filter(), reduce()
   - Closures, nonlocal
   - Decorators (basic, with args, stacking, @wraps)
   - functools.lru_cache, functools.partial
   - Recursion, tail recursion concept
   - Generators (yield, yield from, generator expressions)
   - itertools (chain, product, permutations, combinations, groupby,
               islice, count, cycle, repeat, starmap, zip_longest)
   - Type hints (PEP 484)
 
 Difficulty: Medium to Hard (3 YOE Python Backend Developer)
 Instructions: Try solving YOURSELF before looking at the solution.
=============================================================================
"""

# ============================================================================
# SECTION 1: FUNCTION BASICS (Keyword/Positional, *args, **kwargs, Docstrings)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 1: Build a Flexible Query Builder Using *args and **kwargs
# ────────────────────────────────────────────────────────────────────────────
# Create a function that builds a SQL-like filter string.
# It should accept table name, columns (*args), and filters (**kwargs).
#
# Example:
#   build_query("users", "name", "email", age=25, city="Bangalore")
#   → "SELECT name, email FROM users WHERE age = 25 AND city = 'Bangalore'"
#
# Why asked? Tests *args/**kwargs + string building — real backend work.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def build_query(table, *columns, **filters):
    """
    Build a SQL-like SELECT query string.

    Args:
        table (str): Table name to query.
        *columns: Column names to select. If empty, selects all (*).
        **filters: WHERE conditions as keyword arguments.

    Returns:
        str: The constructed query string.
    """
    cols = ", ".join(columns) if columns else "*"
    query = f"SELECT {cols} FROM {table}"
    
    if filters:
        conditions = []
        for key, value in filters.items():
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
        query += " WHERE " + " AND ".join(conditions)
    
    return query

assert build_query("users", "name", "email", age=25, city="Bangalore") == \
    "SELECT name, email FROM users WHERE age = 25 AND city = 'Bangalore'"
assert build_query("products") == "SELECT * FROM products"
assert build_query("orders", "id", status="pending") == \
    "SELECT id FROM orders WHERE status = 'pending'"
print("✅ Exercise 1 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 2: Keyword-Only and Positional-Only Arguments
# ────────────────────────────────────────────────────────────────────────────
# Create a function `create_response` where:
#   - `status_code` MUST be positional-only (/)
#   - `data` is normal
#   - `message` and `headers` MUST be keyword-only (*)
#
# Why asked? Tests Python 3.8+ syntax — shows modern Python knowledge.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def create_response(status_code, /, data=None, *, message="OK", headers=None):
    """
    Create an API response dict.
    
    Args:
        status_code: HTTP status (positional-only).
        data: Response body (normal arg).
        message: Status message (keyword-only).
        headers: Response headers (keyword-only).
    
    Returns:
        dict: Structured API response.
    """
    return {
        "status": status_code,
        "message": message,
        "data": data,
        "headers": headers or {}
    }

# ✅ Valid calls:
r1 = create_response(200, {"id": 1}, message="Created", headers={"X-Token": "abc"})
assert r1["status"] == 200
assert r1["message"] == "Created"

r2 = create_response(404, message="Not Found")
assert r2["data"] is None

# ❌ These should fail — verify:
try:
    create_response(status_code=200)  # status_code is positional-only!
    assert False, "Should have raised TypeError"
except TypeError:
    pass

try:
    create_response(200, {}, "Custom Message")  # message is keyword-only!
    assert False, "Should have raised TypeError"
except TypeError:
    pass

print("✅ Exercise 2 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 3: Function Arguments Unpacking — Real Scenario
# ────────────────────────────────────────────────────────────────────────────
# You receive a list of user dicts from an API. Pass each dict as kwargs 
# to a registration function. Also unpack a tuple as positional args.
#
# Why asked? Tests * and ** unpacking — used daily in backend code.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def register_user(name, email, role="user"):
    return {"name": name, "email": email, "role": role, "registered": True}

# Unpack dicts as kwargs
users_data = [
    {"name": "Alice", "email": "alice@test.com", "role": "admin"},
    {"name": "Bob", "email": "bob@test.com"},
]

registered = [register_user(**user) for user in users_data]
assert registered[0]["role"] == "admin"
assert registered[1]["role"] == "user"  # Default

# Unpack tuple/list as positional args
def calculate(operation, a, b):
    ops = {"+": a + b, "-": a - b, "*": a * b, "/": a / b}
    return ops.get(operation)

tasks = [("+", 10, 5), ("-", 20, 8), ("*", 3, 7)]
results = [calculate(*task) for task in tasks]
assert results == [15, 12, 21]

print("✅ Exercise 3 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 4: Docstring Parsing (Introspection)
# ────────────────────────────────────────────────────────────────────────────
# Write a function that extracts the Args section from a Google-style 
# docstring and returns a dict of {param_name: description}.
#
# Why asked? Tests __doc__, string parsing — metaprogramming awareness.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def parse_docstring_args(func):
    """Extract parameter names and descriptions from Google-style docstring."""
    doc = func.__doc__
    if not doc:
        return {}
    
    args_dict = {}
    in_args_section = False
    
    for line in doc.split("\n"):
        stripped = line.strip()
        if stripped.startswith("Args:"):
            in_args_section = True
            continue
        elif stripped.startswith("Returns:") or stripped.startswith("Raises:"):
            in_args_section = False
            continue
        
        if in_args_section and stripped:
            # Parse "param_name (type): description" or "param_name: description"
            if ":" in stripped:
                param_part, desc = stripped.split(":", 1)
                # Remove type annotation if present: "name (str)" → "name"
                param_name = param_part.split("(")[0].strip()
                if param_name.startswith("*"):
                    param_name = param_name.lstrip("*")
                args_dict[param_name] = desc.strip()
    
    return args_dict

# Test with our build_query function
result = parse_docstring_args(build_query)
assert "table" in result
assert "columns" in result
assert "filters" in result
assert "Table name" in result["table"]
print("✅ Exercise 4 passed")


# ============================================================================
# SECTION 2: FIRST-CLASS FUNCTIONS & HIGHER-ORDER FUNCTIONS
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 5: Event Dispatcher Using Functions as Objects
# ────────────────────────────────────────────────────────────────────────────
# Build an event system where handlers are registered as functions.
# Supports multiple handlers per event and wildcard (*) handlers.
#
# Why asked? Tests first-class functions — core backend pattern for
# event-driven architecture (Django signals, webhooks, etc.)
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from collections import defaultdict

class EventDispatcher:
    """Event system using functions as first-class objects."""
    
    def __init__(self):
        self._handlers = defaultdict(list)
        self._log = []
    
    def on(self, event_name, handler):
        """Register a handler for an event."""
        self._handlers[event_name].append(handler)
    
    def emit(self, event_name, **data):
        """Trigger an event, calling all registered handlers."""
        results = []
        # Call specific handlers
        for handler in self._handlers.get(event_name, []):
            results.append(handler(event_name, **data))
        # Call wildcard handlers
        for handler in self._handlers.get("*", []):
            results.append(handler(event_name, **data))
        return results

# Test
dispatcher = EventDispatcher()
log = []

def on_user_created(event, **data):
    log.append(f"User created: {data['name']}")
    return "user_handler_done"

def on_any_event(event, **data):
    log.append(f"[LOG] {event}: {data}")
    return "wildcard_done"

dispatcher.on("user_created", on_user_created)
dispatcher.on("*", on_any_event)

results = dispatcher.emit("user_created", name="Sid", email="sid@test.com")
assert "user_handler_done" in results
assert "wildcard_done" in results
assert "User created: Sid" in log

# Event with no specific handler, only wildcard catches it
dispatcher.emit("order_placed", order_id=42)
assert any("order_placed" in entry for entry in log)

print("✅ Exercise 5 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 6: Strategy Pattern Using Higher-Order Functions
# ────────────────────────────────────────────────────────────────────────────
# Implement a pricing engine where discount strategy is passed as a function.
#
# Why asked? Tests higher-order functions + strategy pattern — design question.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def no_discount(price):
    return price

def percentage_discount(percent):
    """Returns a discount function (closure!)."""
    def apply(price):
        return price * (1 - percent / 100)
    return apply

def flat_discount(amount):
    """Returns a flat discount function."""
    def apply(price):
        return max(0, price - amount)
    return apply

def buy_one_get_one(price):
    """50% off."""
    return price * 0.5

def calculate_total(items, discount_strategy=no_discount):
    """Higher-order function: takes a discount function as argument."""
    subtotal = sum(items)
    return round(discount_strategy(subtotal), 2)

items = [100, 200, 300]  # Total: 600

assert calculate_total(items) == 600                          # No discount
assert calculate_total(items, percentage_discount(10)) == 540  # 10% off
assert calculate_total(items, flat_discount(50)) == 550        # ₹50 off
assert calculate_total(items, buy_one_get_one) == 300          # BOGO

print("✅ Exercise 6 passed")


# ============================================================================
# SECTION 3: LAMBDA, MAP, FILTER, REDUCE
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 7: Data Pipeline Using map, filter, reduce
# ────────────────────────────────────────────────────────────────────────────
# Process a list of e-commerce orders:
#   1. Filter: only completed orders
#   2. Map: extract order amounts (apply tax)
#   3. Reduce: calculate total revenue
#
# Why asked? Classic functional pipeline — tests all three.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from functools import reduce

orders = [
    {"id": 1, "amount": 500, "status": "completed"},
    {"id": 2, "amount": 300, "status": "pending"},
    {"id": 3, "amount": 1200, "status": "completed"},
    {"id": 4, "amount": 800, "status": "cancelled"},
    {"id": 5, "amount": 450, "status": "completed"},
]

TAX_RATE = 0.18

# Functional approach:
completed = filter(lambda o: o["status"] == "completed", orders)
taxed_amounts = map(lambda o: o["amount"] * (1 + TAX_RATE), completed)
total_revenue = reduce(lambda acc, x: acc + x, taxed_amounts, 0)

assert total_revenue == (500 + 1200 + 450) * 1.18
print(f"  Total revenue: ₹{total_revenue:.2f}")

# Pythonic equivalent (preferred in production):
total_pythonic = sum(
    o["amount"] * (1 + TAX_RATE)
    for o in orders
    if o["status"] == "completed"
)
assert total_pythonic == total_revenue

print("✅ Exercise 7 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 8: Lambda Sorting Challenges
# ────────────────────────────────────────────────────────────────────────────
# Sort data using lambda keys in various tricky ways.
#
# Why asked? Lambda sorting comes up in almost every Python interview.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:

# a) Sort strings by last character
words = ["hello", "world", "apple", "code", "zen"]
by_last = sorted(words, key=lambda w: w[-1])
assert by_last == ["world", "apple", "code", "zen", "hello"]

# b) Sort dicts by nested value
users = [
    {"name": "Alice", "scores": {"math": 90, "eng": 80}},
    {"name": "Bob", "scores": {"math": 70, "eng": 95}},
    {"name": "Charlie", "scores": {"math": 85, "eng": 85}},
]
by_total_score = sorted(users, key=lambda u: sum(u["scores"].values()), reverse=True)
assert by_total_score[0]["name"] == "Alice"    # 170
assert by_total_score[-1]["name"] == "Bob"     # 165

# c) Sort by multiple criteria: first by status (completed first), then by amount desc
orders_to_sort = [
    {"id": 1, "amount": 500, "status": "pending"},
    {"id": 2, "amount": 300, "status": "completed"},
    {"id": 3, "amount": 800, "status": "completed"},
    {"id": 4, "amount": 200, "status": "pending"},
]
priority = {"completed": 0, "pending": 1, "cancelled": 2}
sorted_orders = sorted(orders_to_sort, key=lambda o: (priority[o["status"]], -o["amount"]))
assert sorted_orders[0]["id"] == 3  # completed, highest amount
assert sorted_orders[1]["id"] == 2  # completed, lower amount
assert sorted_orders[2]["id"] == 1  # pending, highest amount

# d) Sort IPs numerically
ips = ["192.168.1.10", "192.168.1.2", "10.0.0.1", "192.168.1.1"]
sorted_ips = sorted(ips, key=lambda ip: tuple(int(p) for p in ip.split(".")))
assert sorted_ips == ["10.0.0.1", "192.168.1.1", "192.168.1.2", "192.168.1.10"]

print("✅ Exercise 8 passed")


# ============================================================================
# SECTION 4: CLOSURES & NONLOCAL
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 9: Build a Running Average Calculator (Closure)
# ────────────────────────────────────────────────────────────────────────────
# Create a closure that keeps a running average of all values passed to it.
# Each call should return the current average.
#
# Why asked? Classic closure + nonlocal question — tests state retention.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def make_running_average():
    """Closure that maintains running average."""
    total = 0
    count = 0
    
    def averager(new_value):
        nonlocal total, count
        total += new_value
        count += 1
        return total / count
    
    return averager

avg = make_running_average()
assert avg(10) == 10.0
assert avg(20) == 15.0
assert avg(30) == 20.0
assert avg(40) == 25.0

# Independent instance
avg2 = make_running_average()
assert avg2(100) == 100.0  # Not affected by avg's state

print("✅ Exercise 9 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 10: Closure — Late Binding Gotcha (Interview Favourite!)
# ────────────────────────────────────────────────────────────────────────────
# What does this print? Fix it.
#
# Why asked? THE most common closure interview trick question.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:

# THE BUG — Late Binding:
functions_buggy = []
for i in range(5):
    functions_buggy.append(lambda: i)  # All lambdas capture the VARIABLE i, not its value!

# All return 4 (last value of i) — NOT 0,1,2,3,4!
results_buggy = [f() for f in functions_buggy]
assert results_buggy == [4, 4, 4, 4, 4]  # 😱 Surprise!
print(f"  Buggy results: {results_buggy}")

# FIX 1 — Default argument (captures value at definition time):
functions_fix1 = []
for i in range(5):
    functions_fix1.append(lambda i=i: i)  # i=i captures current value!

results_fix1 = [f() for f in functions_fix1]
assert results_fix1 == [0, 1, 2, 3, 4]  # ✅

# FIX 2 — Using closure factory:
def make_func(x):
    return lambda: x

functions_fix2 = [make_func(i) for i in range(5)]
results_fix2 = [f() for f in functions_fix2]
assert results_fix2 == [0, 1, 2, 3, 4]  # ✅

print("✅ Exercise 10 passed — late binding gotcha understood")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 11: Closure as a Lightweight Object (Counter with Reset)
# ────────────────────────────────────────────────────────────────────────────
# Create a counter using closures that supports increment, decrement,
# get_value, and reset — without using a class.
#
# Why asked? Tests closure for state — "can you do OOP without classes?"
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def make_counter(initial=0):
    """Counter using closure — returns a dict of operations."""
    value = initial
    
    def increment(n=1):
        nonlocal value
        value += n
        return value
    
    def decrement(n=1):
        nonlocal value
        value -= n
        return value
    
    def get_value():
        return value
    
    def reset():
        nonlocal value
        value = initial
        return value
    
    return {
        "increment": increment,
        "decrement": decrement,
        "get": get_value,
        "reset": reset
    }

c = make_counter(10)
assert c["get"]() == 10
assert c["increment"]() == 11
assert c["increment"](5) == 16
assert c["decrement"](3) == 13
assert c["reset"]() == 10

print("✅ Exercise 11 passed")


# ============================================================================
# SECTION 5: DECORATORS (Core Interview Topic!)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 12: Timer + Logger Decorator (Basic Decorator)
# ────────────────────────────────────────────────────────────────────────────
# Create a decorator that logs function name, args, return value, and 
# execution time.
#
# Why asked? THE most asked decorator question — every company asks this.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import time
from functools import wraps

def log_and_time(func):
    """Decorator that logs execution details and timing."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        print(f"  → Calling {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  ← {func.__name__} returned {result} in {elapsed:.6f}s")
        return result
    return wrapper

@log_and_time
def add(a, b):
    """Add two numbers."""
    return a + b

result = add(10, 20)
assert result == 30
assert add.__name__ == "add"      # @wraps preserves name
assert add.__doc__ == "Add two numbers."  # @wraps preserves docstring
print("✅ Exercise 12 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 13: Retry Decorator WITH Arguments
# ────────────────────────────────────────────────────────────────────────────
# Create a decorator that retries a function up to `max_retries` times
# if it raises an exception, with a configurable delay.
#
# Why asked? Tests 3-level decorator pattern — common in production code.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def retry(max_retries=3, delay=0, exceptions=(Exception,)):
    """Decorator factory: retry on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        if delay:
                            time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# Test — function that fails first 2 times, succeeds on 3rd
call_count = 0

@retry(max_retries=3, exceptions=(ValueError,))
def flaky_api_call():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("API timeout")
    return "success"

call_count = 0
result = flaky_api_call()
assert result == "success"
assert call_count == 3  # Called 3 times

# Test — exhausts retries and raises
call_count = 0

@retry(max_retries=2, exceptions=(ValueError,))
def always_fails():
    global call_count
    call_count += 1
    raise ValueError("Always broken")

call_count = 0
try:
    always_fails()
    assert False, "Should have raised"
except ValueError:
    assert call_count == 2  # Tried twice, then raised

print("✅ Exercise 13 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 14: Stacking Decorators — Auth + Validate + Log
# ────────────────────────────────────────────────────────────────────────────
# Stack three decorators on an API handler to show execution order.
#
# Why asked? Tests understanding of decorator stacking order.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
execution_order = []

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        execution_order.append("auth_check")
        # Simulate auth check
        return func(*args, **kwargs)
    return wrapper

def validate_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        execution_order.append("validation")
        return func(*args, **kwargs)
    return wrapper

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        execution_order.append("logging")
        result = func(*args, **kwargs)
        execution_order.append("log_response")
        return result
    return wrapper

@log_request        # 3rd to wrap = OUTERMOST = runs FIRST
@auth_required      # 2nd to wrap
@validate_input     # 1st to wrap = INNERMOST = runs LAST (closest to func)
def create_order(user_id, item):
    execution_order.append("handler")
    return {"user": user_id, "item": item, "status": "created"}

execution_order.clear()
result = create_order(1, "laptop")

# Execution order: log → auth → validate → handler → log_response
assert execution_order == ["logging", "auth_check", "validation", "handler", "log_response"]
assert result["status"] == "created"
assert create_order.__name__ == "create_order"  # @wraps preserved

print(f"  Execution order: {execution_order}")
print("✅ Exercise 14 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 15: Class-Based Decorator (Callable Object)
# ────────────────────────────────────────────────────────────────────────────
# Implement a decorator using a class that counts how many times 
# a function has been called and stores call history.
#
# Why asked? Tests __call__ + decorator patterns — advanced but important.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
class CallTracker:
    """Class-based decorator that tracks function calls."""
    
    def __init__(self, func):
        self.func = func
        self.call_count = 0
        self.call_history = []
        # Preserve original function metadata
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
    
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        result = self.func(*args, **kwargs)
        self.call_history.append({
            "call_number": self.call_count,
            "args": args,
            "kwargs": kwargs,
            "result": result
        })
        return result

@CallTracker
def multiply(a, b):
    """Multiply two numbers."""
    return a * b

assert multiply(3, 4) == 12
assert multiply(5, 6) == 30
assert multiply(7, 8) == 56

assert multiply.call_count == 3
assert multiply.call_history[0]["result"] == 12
assert multiply.__name__ == "multiply"

print("✅ Exercise 15 passed")


# ============================================================================
# SECTION 6: FUNCTOOLS — lru_cache & partial
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 16: lru_cache for Expensive Computation
# ────────────────────────────────────────────────────────────────────────────
# Implement a function that computes the nth step of a staircase problem:
# "How many ways to climb n stairs if you can take 1, 2, or 3 steps?"
# Use lru_cache to make it efficient.
#
# Why asked? Classic DP problem — tests lru_cache practical usage.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from functools import lru_cache

@lru_cache(maxsize=256)
def climb_stairs(n):
    """Count ways to climb n stairs taking 1, 2, or 3 steps at a time."""
    if n < 0:
        return 0
    if n == 0:
        return 1
    return climb_stairs(n - 1) + climb_stairs(n - 2) + climb_stairs(n - 3)

assert climb_stairs(1) == 1   # [1]
assert climb_stairs(2) == 2   # [1+1, 2]
assert climb_stairs(3) == 4   # [1+1+1, 1+2, 2+1, 3]
assert climb_stairs(4) == 7
assert climb_stairs(30) == 53798080  # Fast with cache!

# Check cache effectiveness
info = climb_stairs.cache_info()
print(f"  Cache: hits={info.hits}, misses={info.misses}")
assert info.hits > 0  # Cache was actually used

climb_stairs.cache_clear()  # Clean up

print("✅ Exercise 16 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 17: functools.partial — Pre-configured Functions
# ────────────────────────────────────────────────────────────────────────────
# Create pre-configured API request functions using partial.
#
# Why asked? Tests partial for real-world factory patterns.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from functools import partial

def make_request(method, url, headers=None, body=None, timeout=30):
    """Simulate an HTTP request."""
    return {
        "method": method,
        "url": url,
        "headers": headers or {},
        "body": body,
        "timeout": timeout
    }

# Create specialized request functions
get = partial(make_request, "GET")
post = partial(make_request, "POST")
put = partial(make_request, "PUT")
delete = partial(make_request, "DELETE")

# Pre-configured for a specific API
api_get = partial(get, headers={"Authorization": "Bearer token123"}, timeout=10)

# Usage
r1 = get("/users")
assert r1["method"] == "GET"
assert r1["url"] == "/users"
assert r1["timeout"] == 30  # Default

r2 = post("/users", body={"name": "Sid"})
assert r2["method"] == "POST"
assert r2["body"] == {"name": "Sid"}

r3 = api_get("/profile")
assert r3["headers"]["Authorization"] == "Bearer token123"
assert r3["timeout"] == 10

# partial preserves func info
assert get.func is make_request
assert get.args == ("GET",)
assert api_get.keywords["timeout"] == 10

print("✅ Exercise 17 passed")


# ============================================================================
# SECTION 7: RECURSION
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 18: Recursive Directory Tree (Practical Backend Problem)
# ────────────────────────────────────────────────────────────────────────────
# Given a nested dict representing a file system, create a tree display.
# Also implement a search function to find all paths to a file.
#
# Why asked? Recursion on tree structures — real backend file/config patterns.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def print_tree(structure, prefix="", is_last=True, result=None):
    """Generate a tree display string from nested dict."""
    if result is None:
        result = []
    
    if isinstance(structure, dict):
        items = list(structure.items())
        for i, (name, children) in enumerate(items):
            is_last_item = (i == len(items) - 1)
            connector = "└── " if is_last_item else "├── "
            result.append(f"{prefix}{connector}{name}")
            extension = "    " if is_last_item else "│   "
            if isinstance(children, dict):
                print_tree(children, prefix + extension, is_last_item, result)
    
    return result

def find_paths(structure, target, current_path=""):
    """Recursively find all paths to a target file."""
    paths = []
    if isinstance(structure, dict):
        for name, children in structure.items():
            new_path = f"{current_path}/{name}" if current_path else name
            if name == target:
                paths.append(new_path)
            if isinstance(children, dict):
                paths.extend(find_paths(children, target, new_path))
    return paths

# Test
file_system = {
    "src": {
        "models": {
            "user.py": None,
            "order.py": None,
        },
        "views": {
            "user.py": None,  # Same filename in different path
        },
        "utils.py": None,
    },
    "tests": {
        "test_user.py": None,
    },
    "README.md": None,
}

tree = print_tree(file_system)
assert len(tree) > 0
assert any("src" in line for line in tree)

# Find all "user.py" files
paths = find_paths(file_system, "user.py")
assert len(paths) == 2
assert "src/models/user.py" in paths
assert "src/views/user.py" in paths

print("  Tree:")
for line in tree:
    print(f"  {line}")
print("✅ Exercise 18 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 19: Tail Recursion vs Regular Recursion
# ────────────────────────────────────────────────────────────────────────────
# Implement both versions of sum(1..n), show Python's limitation,
# and convert to iterative.
#
# Why asked? Tests understanding of why Python doesn't optimize tail calls.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:

# Regular recursion (NOT tail recursive — pending addition)
def sum_regular(n):
    if n <= 0:
        return 0
    return n + sum_regular(n - 1)  # Addition happens AFTER recursive call

# Tail recursive (last operation IS the recursive call)
def sum_tail(n, accumulator=0):
    if n <= 0:
        return accumulator
    return sum_tail(n - 1, accumulator + n)  # Nothing after this call

# Both give same results
assert sum_regular(100) == 5050
assert sum_tail(100) == 5050

# But Python doesn't optimize tail recursion:
import sys
old_limit = sys.getrecursionlimit()

try:
    # This will hit recursion limit for large n
    # sum_regular(10000)  # RecursionError!
    pass
except RecursionError:
    pass

# ✅ Best practice in Python — use iteration:
def sum_iterative(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

assert sum_iterative(100) == 5050
assert sum_iterative(1_000_000) == 500000500000  # No recursion limit!

# Or even better — math formula:
def sum_formula(n):
    return n * (n + 1) // 2

assert sum_formula(100) == 5050

print("✅ Exercise 19 passed — tail recursion concept understood")


# ============================================================================
# SECTION 8: GENERATORS (yield, yield from, generator expressions)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 20: Generator Pipeline — Log File Processor
# ────────────────────────────────────────────────────────────────────────────
# Build a chain of generators that processes log lines lazily:
#   1. Read lines (simulated)
#   2. Filter ERROR lines
#   3. Extract timestamps and messages
#   4. Format output
#
# Why asked? Generator pipelines are THE backend pattern for streaming data.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def read_logs(lines):
    """Stage 1: Yield each log line."""
    for line in lines:
        yield line.strip()

def filter_errors(lines):
    """Stage 2: Yield only ERROR lines."""
    for line in lines:
        if "ERROR" in line:
            yield line

def parse_log(lines):
    """Stage 3: Parse into structured dicts."""
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) >= 3:
            yield {"timestamp": parts[0], "level": parts[1], "message": parts[2]}

def format_alerts(records):
    """Stage 4: Format for alerting."""
    for record in records:
        yield f"🚨 [{record['timestamp']}] {record['message']}"

# Simulated log data
raw_logs = [
    "2026-03-02T10:00:00 INFO User logged in",
    "2026-03-02T10:01:00 ERROR Database connection timeout",
    "2026-03-02T10:02:00 INFO Order placed",
    "2026-03-02T10:03:00 ERROR Payment gateway unreachable",
    "2026-03-02T10:04:00 WARNING High memory usage",
    "2026-03-02T10:05:00 ERROR Disk space critical",
]

# Chain the generators (lazy — nothing executes until we consume)
pipeline = format_alerts(parse_log(filter_errors(read_logs(raw_logs))))

# NOW it executes — one item at a time through the whole pipeline
alerts = list(pipeline)
assert len(alerts) == 3
assert "Database connection timeout" in alerts[0]
assert "Payment gateway unreachable" in alerts[1]
assert "Disk space critical" in alerts[2]

print("✅ Exercise 20 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 21: yield from — Flatten Nested Structures
# ────────────────────────────────────────────────────────────────────────────
# Use yield from to:
#   a) Chain multiple generators
#   b) Recursively flatten nested iterables
#   c) Walk a tree structure
#
# Why asked? yield from is elegant and often asked as a follow-up to
# "do you know generators?"
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:

# a) Chain generators with yield from
def frontend_tasks():
    yield "Build HTML"
    yield "Compile CSS"

def backend_tasks():
    yield "Setup DB"
    yield "Write API"

def devops_tasks():
    yield "Docker build"
    yield "Deploy"

def all_tasks():
    yield from frontend_tasks()
    yield from backend_tasks()
    yield from devops_tasks()

tasks = list(all_tasks())
assert len(tasks) == 6
assert tasks[0] == "Build HTML"
assert tasks[-1] == "Deploy"

# b) Recursive flatten using yield from
def flatten_gen(iterable):
    """Recursively flatten any nested iterable using yield from."""
    for item in iterable:
        if isinstance(item, (list, tuple)):
            yield from flatten_gen(item)
        else:
            yield item

nested = [1, [2, 3], [4, [5, [6, 7]]], 8]
assert list(flatten_gen(nested)) == [1, 2, 3, 4, 5, 6, 7, 8]

# c) Walk a tree (nested dict) — yield all leaf values
def walk_tree(tree, path=""):
    """Yield (path, value) for every leaf in a nested dict."""
    for key, value in tree.items():
        current = f"{path}.{key}" if path else key
        if isinstance(value, dict):
            yield from walk_tree(value, current)
        else:
            yield (current, value)

config = {
    "db": {"host": "localhost", "port": 5432},
    "cache": {"redis": {"host": "127.0.0.1", "port": 6379}},
    "debug": True
}

leaves = dict(walk_tree(config))
assert leaves["db.host"] == "localhost"
assert leaves["cache.redis.port"] == 6379
assert leaves["debug"] == True

print("✅ Exercise 21 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 22: Generator Expressions — Memory Comparison
# ────────────────────────────────────────────────────────────────────────────
# Show generator expressions used with built-in functions.
#
# Why asked? Tests understanding of lazy vs eager evaluation.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import sys

# Memory comparison
list_comp = [x ** 2 for x in range(1_000_000)]
gen_expr = (x ** 2 for x in range(1_000_000))

list_size = sys.getsizeof(list_comp)
gen_size = sys.getsizeof(gen_expr)

print(f"  List: {list_size:,} bytes vs Generator: {gen_size:,} bytes")
assert gen_size < 200  # Generator is tiny!
assert list_size > 1_000_000  # List is huge!

# Generator expressions directly in functions (no extra parentheses needed):
numbers = range(1, 101)

# sum of squares
assert sum(x ** 2 for x in numbers) == 338350

# any/all with generators
data = [2, 4, 6, 8, 10]
assert all(x % 2 == 0 for x in data)  # All even?
assert any(x > 5 for x in data)        # Any > 5?
assert not any(x < 0 for x in data)    # Any negative?

# max with generator
words = ["hello", "world", "programming", "python"]
longest = max(words, key=lambda w: len(w))
assert longest == "programming"

# Join with generator
csv_line = ",".join(str(x) for x in [1, 2, 3, 4, 5])
assert csv_line == "1,2,3,4,5"

# ⚠️ Generator is single-use!
gen = (x for x in [1, 2, 3])
assert list(gen) == [1, 2, 3]
assert list(gen) == []  # Empty! Already exhausted!

print("✅ Exercise 22 passed")

# Clean up large list
del list_comp


# ============================================================================
# SECTION 9: ITERTOOLS (Complete Coverage)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 23: itertools for Real-World Scenarios
# ────────────────────────────────────────────────────────────────────────────
# Solve practical problems using itertools functions.
#
# Why asked? itertools mastery differentiates mid from senior developers.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import itertools

# --- chain: Merge data from multiple sources ---
api_page1 = [{"id": 1}, {"id": 2}]
api_page2 = [{"id": 3}, {"id": 4}]
api_page3 = [{"id": 5}]

all_records = list(itertools.chain(api_page1, api_page2, api_page3))
assert len(all_records) == 5

# chain.from_iterable — when sources are in a list
pages = [api_page1, api_page2, api_page3]
all_records2 = list(itertools.chain.from_iterable(pages))
assert all_records == all_records2

# --- groupby: Group sorted data ---
transactions = [
    {"type": "credit", "amount": 100},
    {"type": "credit", "amount": 200},
    {"type": "debit", "amount": 50},
    {"type": "debit", "amount": 75},
    {"type": "credit", "amount": 300},
]
# ⚠️ groupby needs SORTED data!
transactions.sort(key=lambda t: t["type"])
grouped = {}
for key, group in itertools.groupby(transactions, key=lambda t: t["type"]):
    grouped[key] = [t["amount"] for t in group]

assert "credit" in grouped
assert "debit" in grouped
assert sum(grouped["credit"]) == 600

# --- islice: Paginate generator results ---
def infinite_users():
    i = 1
    while True:
        yield {"id": i, "name": f"user_{i}"}
        i += 1

page_size = 5
page_2 = list(itertools.islice(infinite_users(), 5, 10))  # Skip 5, take 5
assert len(page_2) == 5
assert page_2[0]["id"] == 6

# --- product: Generate all test combinations ---
methods = ["GET", "POST"]
endpoints = ["/users", "/orders"]
auth_states = [True, False]

test_cases = list(itertools.product(methods, endpoints, auth_states))
assert len(test_cases) == 8  # 2 × 2 × 2
assert ("GET", "/users", True) in test_cases

# --- combinations: Find all pairs for comparison ---
servers = ["server_a", "server_b", "server_c", "server_d"]
server_pairs = list(itertools.combinations(servers, 2))
assert len(server_pairs) == 6  # C(4,2) = 6

# --- permutations: All orderings ---
priorities = ["high", "medium", "low"]
orderings = list(itertools.permutations(priorities))
assert len(orderings) == 6  # 3! = 6

# --- starmap: Apply function to pre-paired arguments ---
pairs = [(2, 5), (3, 2), (10, 3)]
powers = list(itertools.starmap(pow, pairs))
assert powers == [32, 9, 1000]

# --- zip_longest: Handle unequal data ---
names = ["Alice", "Bob", "Charlie"]
scores = [90, 85]
combined = list(itertools.zip_longest(names, scores, fillvalue=0))
assert combined == [("Alice", 90), ("Bob", 85), ("Charlie", 0)]

# --- count: ID generator ---
id_counter = itertools.count(start=1000, step=1)
assert next(id_counter) == 1000
assert next(id_counter) == 1001
assert next(id_counter) == 1002

# --- cycle: Round-robin load balancer ---
servers_cycle = itertools.cycle(["server1", "server2", "server3"])
assignments = [next(servers_cycle) for _ in range(7)]
assert assignments == ["server1", "server2", "server3", "server1", "server2", "server3", "server1"]

# --- repeat: Create default configs ---
defaults = list(itertools.repeat({"status": "pending"}, 3))
assert len(defaults) == 3
# ⚠️ They're the SAME object! Use list comprehension if you need copies.

print("✅ Exercise 23 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 24: itertools — Sliding Window (Interview Classic)
# ────────────────────────────────────────────────────────────────────────────
# Implement a generic sliding window using itertools.
#
# Why asked? Combines islice + generators — common interview pattern.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def sliding_window(iterable, n):
    """Generate sliding windows of size n over iterable."""
    it = iter(iterable)
    window = list(itertools.islice(it, n))
    if len(window) == n:
        yield tuple(window)
    for item in it:
        window = window[1:] + [item]
        yield tuple(window)

# Test
data = [1, 2, 3, 4, 5, 6]
windows = list(sliding_window(data, 3))
assert windows == [(1,2,3), (2,3,4), (3,4,5), (4,5,6)]

# Moving average using sliding window
def moving_average(data, window_size):
    for window in sliding_window(data, window_size):
        yield sum(window) / len(window)

prices = [100, 102, 104, 103, 105, 107, 106]
averages = list(moving_average(prices, 3))
assert len(averages) == 5
assert abs(averages[0] - 102.0) < 0.01  # avg(100,102,104)

print("✅ Exercise 24 passed")


# ============================================================================
# SECTION 10: TYPE HINTS (PEP 484)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 25: Type Hints — Fully Typed Backend Functions
# ────────────────────────────────────────────────────────────────────────────
# Write properly typed functions covering all common type hint patterns.
#
# Why asked? Type hints are mandatory in professional Python — FastAPI, 
# Pydantic, enterprise code all require them.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from typing import Optional, Union, Any, Callable, TypeVar, Protocol, List

# a) Basic function with type hints
def create_user(
    name: str, 
    age: int, 
    email: Optional[str] = None,
    roles: Optional[List[str]] = None  # Use typing.List for Python 3.9 compat
) -> dict:
    """Create a user dict with full type hints."""
    return {
        "name": name,
        "age": age,
        "email": email,
        "roles": roles or ["user"],
    }

user = create_user("Sid", 25, email="sid@test.com", roles=["admin"])
assert user["name"] == "Sid"
assert user["roles"] == ["admin"]

# b) Callback type hint
def apply_transform(
    data: list[int],
    transform: Callable[[int], int]  # Function that takes int, returns int
) -> list[int]:
    return [transform(x) for x in data]

result = apply_transform([1, 2, 3], lambda x: x * 10)
assert result == [10, 20, 30]

# c) TypeVar for generic functions
T = TypeVar("T")

def first_or_default(items: list[T], default: T) -> T:
    """Return first item or default — works with any type."""
    return items[0] if items else default

assert first_or_default([1, 2, 3], 0) == 1
assert first_or_default([], "fallback") == "fallback"

# d) Protocol (structural subtyping — duck typing with type safety)
class Serializable(Protocol):
    def to_dict(self) -> dict: ...

class User:
    def __init__(self, name: str):
        self.name = name
    def to_dict(self) -> dict:
        return {"name": self.name}

class Order:
    def __init__(self, id: int):
        self.id = id
    def to_dict(self) -> dict:
        return {"id": self.id}

def serialize(obj: Serializable) -> dict:
    """Accepts any object with a to_dict() method."""
    return obj.to_dict()

assert serialize(User("Sid")) == {"name": "Sid"}
assert serialize(Order(42)) == {"id": 42}

# e) Union types
def process_id(id_value: Union[int, str]) -> str:
    """Accept int or str ID, always return str."""
    return str(id_value)

assert process_id(42) == "42"
assert process_id("abc") == "abc"

print("✅ Exercise 25 passed")


# ============================================================================
# SECTION 11: MIXED INTERVIEW QUESTIONS (Combining Multiple Concepts)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 26: Build a Middleware Pipeline (Decorators + HOF + Closures)
# ────────────────────────────────────────────────────────────────────────────
# Implement an Express.js-style middleware system where each middleware
# can modify request/response and call next().
#
# Why asked? Combines closures + HOF + decorator ideas — real backend.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def create_app():
    """Create a simple middleware-based app."""
    middlewares = []
    
    def use(middleware):
        """Register a middleware function."""
        middlewares.append(middleware)
    
    def handle(request):
        """Process request through all middlewares then handler."""
        index = 0
        
        def next_middleware():
            nonlocal index
            if index < len(middlewares):
                mw = middlewares[index]
                index += 1
                return mw(request, next_middleware)
            return None
        
        return next_middleware()
    
    return use, handle

# Build the app
use, handle = create_app()

# Middleware 1: Auth
def auth_middleware(request, next_fn):
    if "token" not in request:
        return {"error": "Unauthorized", "status": 401}
    request["user"] = "Sid"  # Attach user from token
    return next_fn()

# Middleware 2: Logging
def logging_middleware(request, next_fn):
    request["logged"] = True
    response = next_fn()
    return response

# Middleware 3: Handler (last in chain)
def handler(request, next_fn):
    return {"data": f"Hello {request['user']}", "status": 200}

use(auth_middleware)
use(logging_middleware)
use(handler)

# Test with auth
response = handle({"path": "/api", "token": "abc"})
assert response["status"] == 200
assert "Hello Sid" in response["data"]

# Test without auth
response = handle({"path": "/api"})
assert response["status"] == 401

print("✅ Exercise 26 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 27: Memoized API Client with TTL (Decorator + Generator + Closure)
# ────────────────────────────────────────────────────────────────────────────
# Create a caching decorator that expires after TTL seconds.
# functools.lru_cache doesn't support TTL, so build your own!
#
# Why asked? Shows you can go beyond built-in tools — senior-level thinking.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def cache_with_ttl(ttl_seconds):
    """Decorator factory: cache results with time-to-live expiration."""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result  # Cache hit!
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        wrapper.cache = cache
        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

# Test
call_log = []

@cache_with_ttl(ttl_seconds=2)
def fetch_user(user_id):
    call_log.append(f"fetched_{user_id}")
    return {"id": user_id, "name": f"User {user_id}"}

call_log.clear()

# First call — cache miss
r1 = fetch_user(1)
assert len(call_log) == 1

# Second call — cache hit (within TTL)
r2 = fetch_user(1)
assert len(call_log) == 1  # NOT called again!
assert r1 == r2

# Different args — cache miss
r3 = fetch_user(2)
assert len(call_log) == 2

# Verify cache has entries
assert len(fetch_user.cache) == 2

# Clean up
fetch_user.clear_cache()

print("✅ Exercise 27 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 28: Compose Functions (Functional Programming Pattern)
# ────────────────────────────────────────────────────────────────────────────
# Implement compose() and pipe() — apply a sequence of functions.
# compose: right-to-left  |  pipe: left-to-right
#
# Why asked? Tests reduce + higher-order functions — functional mastery.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def compose(*functions):
    """Compose functions right-to-left: compose(f, g, h)(x) = f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

def pipe(*functions):
    """Pipe functions left-to-right: pipe(f, g, h)(x) = h(g(f(x)))"""
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

# Test
double = lambda x: x * 2
add_one = lambda x: x + 1
square = lambda x: x ** 2

# compose: square(add_one(double(5))) = square(11) = 121
assert compose(square, add_one, double)(5) == 121

# pipe: square(add_one(double(5)))... wait, pipe goes left-to-right:
# double(5) = 10, add_one(10) = 11, square(11) = 121
assert pipe(double, add_one, square)(5) == 121

# Different order matters for compose:
# compose(double, add_one, square)(3) = double(add_one(square(3)))
# = double(add_one(9)) = double(10) = 20
assert compose(double, add_one, square)(3) == 20

# Real-world: data processing pipeline
normalize = lambda s: s.strip().lower()
remove_special = lambda s: "".join(c for c in s if c.isalnum() or c == " ")
slugify = lambda s: s.replace(" ", "-")

make_slug = pipe(normalize, remove_special, slugify)
assert make_slug("  Hello World! ") == "hello-world"
assert make_slug("  Python 3.10 Tips!! ") == "python-310-tips"

print("✅ Exercise 28 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 29: Generator-Based Pagination (Real Backend Pattern)
# ────────────────────────────────────────────────────────────────────────────
# Create a generic paginator that lazily fetches and yields pages.
#
# Why asked? Generators for lazy DB pagination — asked in system design.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def paginate(fetch_fn: Callable, page_size: int = 10):
    """
    Generic paginator generator.
    
    Args:
        fetch_fn: Function(offset, limit) → list of items
        page_size: Items per page
    
    Yields:
        Lists of items, one page at a time
    """
    offset = 0
    while True:
        page = fetch_fn(offset, page_size)
        if not page:
            break
        yield page
        if len(page) < page_size:
            break  # Last page
        offset += page_size

# Simulate a database
fake_db = [{"id": i, "name": f"Item {i}"} for i in range(1, 24)]

def fake_query(offset, limit):
    """Simulates: SELECT * FROM items LIMIT {limit} OFFSET {offset}"""
    return fake_db[offset:offset + limit]

# Paginate through results
pages = list(paginate(fake_query, page_size=5))
assert len(pages) == 5  # 23 items / 5 per page = 5 pages
assert len(pages[0]) == 5
assert len(pages[-1]) == 3  # Last page has 3 items
assert pages[0][0]["id"] == 1
assert pages[-1][-1]["id"] == 23

# Total items across all pages
total = sum(len(page) for page in paginate(fake_query, page_size=5))
assert total == 23

print("✅ Exercise 29 passed")


# ============================================================================
# BONUS: TRICKY INTERVIEW QUESTIONS
# ============================================================================

print("\n" + "=" * 60)
print("BONUS: TRICKY FUNCTION QUESTIONS — Predict the Output!")
print("=" * 60)


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q1: What does this decorator return?
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q1: Missing return in decorator ---")

def broken_decorator(func):
    def wrapper(*args, **kwargs):
        print("  Before")
        func(*args, **kwargs)  # ⚠️ Missing return!
        print("  After")
    return wrapper

@broken_decorator
def get_data():
    return {"data": [1, 2, 3]}

result = get_data()
print(f"  result = {result}")  # None! — wrapper doesn't return func's value!
print("⚠️  Always `return func(*args, **kwargs)` in decorators!")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q2: Closure variable scope
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q2: When is the variable captured? ---")

def make_functions():
    fns = []
    for i in range(3):
        def fn():
            return i  # Captures the VARIABLE i, not the VALUE
        fns.append(fn)
    return fns

fns = make_functions()
print(f"  [fn() for fn in fns] = {[fn() for fn in fns]}")  # [2, 2, 2] NOT [0, 1, 2]!
print("⚠️  Late binding! The closure sees i=2 when called. Fix: default arg i=i")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q3: Generator exhaustion
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q3: Why is the second sum 0? ---")

gen = (x for x in range(5))
sum1 = sum(gen)
sum2 = sum(gen)
print(f"  sum1 = {sum1}, sum2 = {sum2}")  # 10, 0!
print("⚠️  Generators are single-use! After exhaustion, they yield nothing.")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q4: *args unpacking gotcha
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q4: What does this print? ---")

def show(*args):
    print(f"  args = {args}")

show([1, 2, 3])      # args = ([1, 2, 3],)  — the LIST is ONE argument!
show(*[1, 2, 3])     # args = (1, 2, 3)     — unpacked into THREE arguments!
print("⚠️  show(list) ≠ show(*list). Without *, the whole list is a single arg.")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q5: Decorator order with print
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q5: What order do decorators execute? ---")

def deco_a(func):
    print("  deco_a applied")
    def wrapper():
        print("  deco_a before")
        func()
        print("  deco_a after")
    return wrapper

def deco_b(func):
    print("  deco_b applied")
    def wrapper():
        print("  deco_b before")
        func()
        print("  deco_b after")
    return wrapper

@deco_a   # 2nd: wraps the result of deco_b
@deco_b   # 1st: wraps greet
def greet():
    print("  Hello!")

print("  --- Calling greet() ---")
greet()
print("⚠️  Application: bottom→top (b then a). Execution: top→down (a then b).")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q6: reduce with no initial value on empty list
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q6: What happens? ---")

try:
    result = reduce(lambda a, b: a + b, [])
    print(f"  result = {result}")
except TypeError as e:
    print(f"  TypeError: {e}")
    print("⚠️  reduce on empty list without initial value raises TypeError!")
    print("  Fix: reduce(func, [], 0) — always provide initial for empty-safety")

# Safe version:
result = reduce(lambda a, b: a + b, [], 0)
assert result == 0


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q7: yield vs return in generator
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q7: What does return do inside a generator? ---")

def gen_with_return():
    yield 1
    yield 2
    return "done"  # Doesn't yield "done"! Sets StopIteration.value
    yield 3        # Never reached!

values = list(gen_with_return())
print(f"  values = {values}")  # [1, 2] — "done" is NOT yielded, 3 is never reached
print("⚠️  return in a generator stops it. The return value goes to StopIteration.value")

# To see the return value:
gen = gen_with_return()
next(gen)  # 1
next(gen)  # 2
try:
    next(gen)
except StopIteration as e:
    print(f"  StopIteration.value = '{e.value}'")  # "done"


print("\n" + "=" * 60)
print("🎉 ALL 29 EXERCISES + 7 TRICKY QUESTIONS COMPLETED! 🎉")
print("   Full Phase 3 Functions coverage achieved.")
print("=" * 60)
