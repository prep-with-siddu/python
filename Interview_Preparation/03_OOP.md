# 03 — Object-Oriented Programming (OOP) — Interview Questions

> **50+ questions covering classes, inheritance, polymorphism, SOLID, design patterns**

---

## 🔹 Section 1: OOP Basics

### Q1. 🟢 What is OOP? What are the 4 pillars?

**Answer:**
OOP = Object-Oriented Programming — organizes code around objects (data + behavior).

| Pillar | Meaning | Python Example |
|--------|---------|----------------|
| **Encapsulation** | Bundle data + methods, restrict access | `_private`, `__mangled` |
| **Abstraction** | Hide complex implementation, show interface | `ABC`, `@abstractmethod` |
| **Inheritance** | Create new class from existing class | `class Dog(Animal)` |
| **Polymorphism** | Same interface, different behavior | Method overriding |

---

### Q2. 🟢 What is a class? What is an object?

**Answer:**
```python
# Class = Blueprint / Template
class Car:
    def __init__(self, brand, speed):
        self.brand = brand     # instance attribute
        self.speed = speed
    
    def accelerate(self):      # instance method
        self.speed += 10

# Object = Instance of a class
car1 = Car("Tesla", 100)  # object 1
car2 = Car("BMW", 120)    # object 2

car1.accelerate()
print(car1.speed)   # 110
print(car2.speed)   # 120 (independent)
```

---

### Q3. 🟢 What is `self` in Python?

**Answer:**
`self` refers to the **current instance** of the class. It's passed automatically.

```python
class User:
    def __init__(self, name):
        self.name = name         # self = current instance
    
    def greet(self):
        return f"Hi, I'm {self.name}"

u = User("Sid")
u.greet()      # Internally: User.greet(u)
```

- `self` is a convention, not a keyword (could use any name, but DON'T)
- Must be the first parameter of instance methods
- NOT needed for `@staticmethod`

---

### Q4. 🟢 What is `__init__`? Is it a constructor?

**Answer:**
`__init__` is the **initializer**, not technically the constructor.

```python
class User:
    def __new__(cls, name):        # Constructor — creates instance
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, name):      # Initializer — sets up instance
        self.name = name

# Flow: __new__ creates → __init__ initializes
u = User("Sid")
```

| Method | Purpose | Returns |
|--------|---------|---------|
| `__new__` | Creates the object | Must return instance |
| `__init__` | Initializes the object | Returns None |

**Interview tip:** Most people say `__init__` is the constructor. Technically wrong, but acceptable.

---

### Q5. 🟡 What are class variables vs instance variables?

**Answer:**
```python
class Employee:
    company = "TechCorp"        # Class variable (shared by all)
    employee_count = 0
    
    def __init__(self, name, salary):
        self.name = name         # Instance variable (unique per object)
        self.salary = salary
        Employee.employee_count += 1

e1 = Employee("Sid", 50000)
e2 = Employee("Raj", 60000)

print(e1.company)       # "TechCorp" (from class)
print(e2.company)       # "TechCorp" (from class)
print(Employee.employee_count)  # 2

# ⚠️ Gotcha: Assigning via instance creates NEW instance variable
e1.company = "NewCorp"
print(e1.company)       # "NewCorp" (instance)
print(e2.company)       # "TechCorp" (still class)
print(Employee.company) # "TechCorp" (still class)
```

---

### Q6. 🟡 What are the different types of methods?

**Answer:**
```python
class MyClass:
    class_var = "shared"
    
    # 1. Instance method — access instance & class
    def instance_method(self):
        return f"instance: {self.class_var}"
    
    # 2. Class method — access class, NOT instance
    @classmethod
    def class_method(cls):
        return f"class: {cls.class_var}"
    
    # 3. Static method — access NEITHER
    @staticmethod
    def static_method():
        return "I'm a utility function"

obj = MyClass()
obj.instance_method()        # Works
MyClass.class_method()       # Works
MyClass.static_method()      # Works
```

| Method Type | First Param | Can Access Instance | Can Access Class |
|------------|-------------|--------------------|-&-----------------|
| Instance | `self` | ✅ | ✅ |
| Class | `cls` | ❌ | ✅ |
| Static | None | ❌ | ❌ |

**When to use `@classmethod`:** Factory methods, alternative constructors.
```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"])

user = User.from_dict({"name": "Sid", "age": 25})
```

---

## 🔹 Section 2: Encapsulation & Access Control

### Q7. 🟡 How does Python handle access control (public, private, protected)?

**Answer:**
Python uses **naming conventions**, not true access modifiers.

```python
class Account:
    def __init__(self):
        self.public = "Anyone"          # Public
        self._protected = "Internal"     # Protected (convention only)
        self.__private = "Name mangled"  # Private (name mangling)

acc = Account()
print(acc.public)           # ✅ Works
print(acc._protected)       # ✅ Works (just a convention)
# print(acc.__private)      # ❌ AttributeError
print(acc._Account__private) # ✅ Works (name mangling)
```

| Prefix | Convention | Accessible? |
|--------|-----------|-------------|
| `name` | Public | Yes |
| `_name` | Protected/Internal | Yes (but shouldn't) |
| `__name` | Private (name mangled) | Via `_ClassName__name` |
| `__name__` | Dunder/Magic | Yes (special Python methods) |

**Key point:** Python has NO true private members. It's all convention. "We're all consenting adults."

---

### Q8. 🟡 What is name mangling?

**Answer:**
When you use `__attr`, Python renames it to `_ClassName__attr` to avoid conflicts in subclasses.

```python
class Parent:
    def __init__(self):
        self.__secret = "parent"

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__secret = "child"  # Different attribute!

c = Child()
print(c._Parent__secret)  # "parent"
print(c._Child__secret)   # "child"
print(c.__dict__)
# {'_Parent__secret': 'parent', '_Child__secret': 'child'}
```

---

### Q9. 🟡 What is `@property`? Why use it?

**Answer:**
`@property` lets you use methods like attributes — getter/setter with validation.

```python
class User:
    def __init__(self, age):
        self._age = age    # Store in private
    
    @property
    def age(self):           # Getter
        return self._age
    
    @age.setter
    def age(self, value):    # Setter with validation
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value
    
    @age.deleter
    def age(self):           # Deleter
        del self._age

user = User(25)
print(user.age)      # 25 (calls getter)
user.age = 30        # (calls setter)
# user.age = -5      # ValueError!
```

**Backend use:** Validate data before setting, computed properties, lazy loading.

---

## 🔹 Section 3: Inheritance

### Q10. 🟢 What is inheritance? Types?

**Answer:**
```python
# Single Inheritance
class Animal:
    def speak(self): return "..."

class Dog(Animal):
    def speak(self): return "Woof!"

# Multiple Inheritance
class Flyable:
    def fly(self): return "Flying!"

class Swimmable:
    def swim(self): return "Swimming!"

class Duck(Flyable, Swimmable):
    pass

d = Duck()
d.fly()   # "Flying!"
d.swim()  # "Swimming!"

# Multilevel Inheritance
class A: pass
class B(A): pass
class C(B): pass   # C → B → A
```

| Type | Example |
|------|---------|
| Single | `Dog(Animal)` |
| Multiple | `Duck(Flyable, Swimmable)` |
| Multilevel | `C(B)`, `B(A)` |
| Hierarchical | `Dog(Animal)`, `Cat(Animal)` |

---

### Q11. 🟡 What is the MRO (Method Resolution Order)?

**Answer:**
MRO determines which method is called in multiple inheritance. Uses **C3 Linearization**.

```python
class A:
    def greet(self): return "A"

class B(A):
    def greet(self): return "B"

class C(A):
    def greet(self): return "C"

class D(B, C):
    pass

print(D.__mro__)
# D → B → C → A → object

print(D().greet())  # "B" (first in MRO after D)
```

**Diamond Problem:**
```
    A
   / \
  B   C
   \ /
    D
```
Python's C3 linearization solves this deterministically.

---

### Q12. 🟡 What is `super()`? How does it work?

**Answer:**
`super()` calls the next class in MRO, not necessarily the parent.

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # Calls Animal.__init__
        self.breed = breed

d = Dog("Rex", "Labrador")
print(d.name, d.breed)  # Rex Labrador
```

**With multiple inheritance:**
```python
class A:
    def __init__(self):
        print("A")
        super().__init__()

class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()

D()  # D → B → C → A (follows MRO!)
```

---

### Q13. 🟡 What is the difference between `isinstance()` and `type()`?

**Answer:**
```python
class Animal: pass
class Dog(Animal): pass

d = Dog()

# type() — exact type only
type(d) == Dog       # True
type(d) == Animal    # False ❌

# isinstance() — checks inheritance chain
isinstance(d, Dog)     # True
isinstance(d, Animal)  # True ✅
isinstance(d, object)  # True

# isinstance with tuple
isinstance(d, (Dog, Animal))  # True (either)
```

**Rule:** Always use `isinstance()` in production code — respects inheritance.

---

## 🔹 Section 4: Polymorphism

### Q14. 🟡 What is polymorphism? Give examples.

**Answer:**
Same interface, different behavior.

```python
# 1. Method Overriding (Runtime Polymorphism)
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

# Same method, different behavior
shapes = [Circle(5), Square(4)]
for shape in shapes:
    print(shape.area())  # 78.5, 16

# 2. Duck Typing
class Cat:
    def speak(self): return "Meow"

class Dog:
    def speak(self): return "Woof"

for animal in [Cat(), Dog()]:
    print(animal.speak())  # Don't care about type

# 3. Operator Overloading
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```

---

### Q15. 🟡 Does Python support method overloading?

**Answer:**
**No.** Python doesn't support traditional method overloading (same name, different signatures).

```python
# ❌ Second definition overwrites the first
class Calculator:
    def add(self, a, b):
        return a + b
    def add(self, a, b, c):
        return a + b + c

calc = Calculator()
# calc.add(1, 2)  # TypeError: missing argument 'c'
```

**Workarounds:**
```python
# 1. Default arguments
def add(self, a, b, c=0):
    return a + b + c

# 2. *args
def add(self, *args):
    return sum(args)

# 3. @singledispatch (Python 3.4+)
from functools import singledispatch

@singledispatch
def process(data):
    raise TypeError(f"Unsupported type: {type(data)}")

@process.register(str)
def _(data):
    return data.upper()

@process.register(int)
def _(data):
    return data * 2

# 4. @overload (type hints only, Python 3.5+)
from typing import overload

@overload
def greet(name: str) -> str: ...
@overload
def greet(name: str, age: int) -> str: ...
```

---

## 🔹 Section 5: Abstract Classes & Interfaces

### Q16. 🟡 What is an abstract class in Python?

**Answer:**
```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    
    @abstractmethod
    def process_payment(self, amount):
        """Must be implemented by subclass"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id):
        pass
    
    def log(self, message):   # Concrete method (optional to override)
        print(f"LOG: {message}")

# ❌ Can't instantiate abstract class
# gateway = PaymentGateway()  # TypeError

# ✅ Must implement ALL abstract methods
class StripeGateway(PaymentGateway):
    def process_payment(self, amount):
        return f"Stripe: charged {amount}"
    
    def refund(self, transaction_id):
        return f"Stripe: refunded {transaction_id}"

gateway = StripeGateway()
gateway.process_payment(100)
gateway.log("Payment processed")  # Inherited
```

---

### Q17. 🟡 What is the difference between an abstract class and an interface?

**Answer:**
Python doesn't have a formal `interface` keyword, but:

| Feature | Abstract Class | Interface (Protocol) |
|---------|---------------|---------------------|
| Module | `abc.ABC` | `typing.Protocol` |
| Can have concrete methods | ✅ Yes | ✅ Yes |
| Can have state | ✅ Yes | ❌ No (convention) |
| Inheritance required | ✅ Yes | ❌ No (structural) |
| Multiple | ✅ Multiple inheritance | ✅ Multiple protocols |

```python
# Protocol (Python 3.8+) — structural typing (duck typing + types)
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:  # Does NOT explicitly inherit Drawable
    def draw(self) -> None:
        print("Drawing circle")

def render(shape: Drawable):  # Type checker accepts Circle
    shape.draw()

render(Circle())  # ✅ Works — Circle has draw()
```

---

## 🔹 Section 6: SOLID Principles

### Q18. 🟡 What are SOLID principles? Explain with Python examples.

**Answer:**

**S — Single Responsibility Principle (SRP)**
```python
# ❌ One class doing too much
class User:
    def __init__(self, name): self.name = name
    def save_to_db(self): ...      # Persistence
    def send_email(self): ...       # Notification
    def generate_report(self): ...  # Reporting

# ✅ Separate responsibilities
class User:
    def __init__(self, name): self.name = name

class UserRepository:
    def save(self, user): ...

class EmailService:
    def send(self, user, message): ...
```

**O — Open/Closed Principle (OCP)**
```python
# Open for extension, closed for modification
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def calculate(self, price): pass

class RegularDiscount(Discount):
    def calculate(self, price): return price * 0.1

class PremiumDiscount(Discount):
    def calculate(self, price): return price * 0.2

# Adding new discount type doesn't modify existing code
class VIPDiscount(Discount):
    def calculate(self, price): return price * 0.3
```

**L — Liskov Substitution Principle (LSP)**
```python
# Subclass should be substitutable for parent
class Bird:
    def fly(self): return "Flying!"

# ❌ Violates LSP
class Penguin(Bird):
    def fly(self): raise Exception("Can't fly!")

# ✅ Better design
class Bird: pass
class FlyingBird(Bird):
    def fly(self): return "Flying!"
class Penguin(Bird):
    def swim(self): return "Swimming!"
```

**I — Interface Segregation Principle (ISP)**
```python
# ❌ Fat interface
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    @abstractmethod
    def eat(self): pass   # Robots don't eat!

# ✅ Segregated interfaces
class Workable(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC):
    @abstractmethod
    def eat(self): pass

class Human(Workable, Eatable):
    def work(self): ...
    def eat(self): ...

class Robot(Workable):
    def work(self): ...
```

**D — Dependency Inversion Principle (DIP)**
```python
# ❌ High-level depends on low-level
class MySQLDatabase:
    def save(self, data): ...

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()   # Tight coupling

# ✅ Depend on abstraction
class Database(ABC):
    @abstractmethod
    def save(self, data): pass

class MySQLDatabase(Database):
    def save(self, data): ...

class PostgresDatabase(Database):
    def save(self, data): ...

class UserService:
    def __init__(self, db: Database):    # Dependency injection
        self.db = db

# Easy to swap
service = UserService(PostgresDatabase())
```

---

## 🔹 Section 7: Design Patterns

### Q19. 🟡 Implement Singleton pattern.

**Answer:**
```python
# Method 1: Using __new__
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)  # True

# Method 2: Using decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connection = "connected"

# Method 3: Module-level (Pythonic way)
# config.py
# settings = Settings()  # Module is only loaded once
```

---

### Q20. 🟡 Implement Factory pattern.

**Answer:**
```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message): pass

class EmailNotification(Notification):
    def send(self, message): return f"Email: {message}"

class SMSNotification(Notification):
    def send(self, message): return f"SMS: {message}"

class PushNotification(Notification):
    def send(self, message): return f"Push: {message}"

class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        factories = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification,
        }
        if channel not in factories:
            raise ValueError(f"Unknown channel: {channel}")
        return factories[channel]()

# Usage
notif = NotificationFactory.create("email")
notif.send("Hello!")
```

---

### Q21. 🟡 Implement Observer pattern.

**Answer:**
```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}
    
    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)
    
    def emit(self, event, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

# Usage
emitter = EventEmitter()
emitter.on("user_created", lambda user: print(f"Welcome {user}!"))
emitter.on("user_created", lambda user: print(f"Sending email to {user}"))

emitter.emit("user_created", "Sid")
# Welcome Sid!
# Sending email to Sid
```

---

### Q22. 🟡 Implement Strategy pattern.

**Answer:**
```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

class BubbleSort(SortStrategy):
    def sort(self, data):
        return sorted(data)  # simplified

class QuickSort(SortStrategy):
    def sort(self, data):
        return sorted(data)  # simplified

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data):
        return self._strategy.sort(data)

# Switch strategy at runtime
sorter = Sorter(QuickSort())
sorter.sort([3, 1, 2])
```

---

## 🔹 Section 8: Advanced OOP

### Q23. 🔴 What are descriptors?

**Answer:**
Descriptors control attribute access. They implement `__get__`, `__set__`, or `__delete__`.

```python
class Validator:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        return getattr(obj, f'_{self.name}', None)
    
    def __set__(self, obj, value):
        if not self.min_val <= value <= self.max_val:
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        setattr(obj, f'_{self.name}', value)

class Product:
    price = Validator(0, 10000)
    quantity = Validator(0, 1000)
    
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

p = Product(100, 5)     # ✅
# p = Product(-1, 5)    # ValueError
```

**Key:** `@property`, `@classmethod`, `@staticmethod` are all descriptors internally.

---

### Q24. 🔴 What are metaclasses?

**Answer:**
A metaclass is a class of a class. It controls how classes are created.

```python
# type is the default metaclass
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>

# Custom metaclass
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connected = True

a = Database()
b = Database()
print(a is b)  # True
```

**When to use:** Rarely. ORMs (Django models), API frameworks, validation.

---

### Q25. 🟡 What is `__slots__`?

**Answer:**
`__slots__` restricts instance attributes and saves memory (no `__dict__`).

```python
class UserWithDict:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class UserWithSlots:
    __slots__ = ['name', 'age']
    def __init__(self, name, age):
        self.name = name
        self.age = age

import sys
u1 = UserWithDict("Sid", 25)
u2 = UserWithSlots("Sid", 25)

print(sys.getsizeof(u1.__dict__))  # 104 bytes
# u2 has no __dict__ → saves ~40-60% memory

# u2.email = "test"  # AttributeError — can't add new attributes
```

**Use when:** Creating millions of instances (e.g., data processing, game objects).

---

### Q26. 🟡 What is `dataclass`? Why use it?

**Answer:**
```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int
    email: str = ""
    tags: list = field(default_factory=list)

# Auto-generates: __init__, __repr__, __eq__
u = User("Sid", 25)
print(u)  # User(name='Sid', age=25, email='', tags=[])

# Frozen (immutable)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError
```

| Feature | Regular Class | `dataclass` | `namedtuple` |
|---------|--------------|-------------|--------------|
| Mutable | ✅ | ✅ (default) | ❌ |
| Default `__init__` | ❌ Manual | ✅ Auto | ✅ Auto |
| `__repr__` | ❌ Manual | ✅ Auto | ✅ Auto |
| `__eq__` | ❌ Manual | ✅ Auto | ✅ Auto |
| Inheritance | ✅ | ✅ | Limited |
| Type hints | Optional | Required | Optional |

---

## 🔹 Section 9: Tricky OOP Questions

### Q27. 🟡 What is the output?

```python
class A:
    x = 1

class B(A):
    pass

class C(A):
    pass

B.x = 2
print(A.x, B.x, C.x)
```

**Answer:** `1 2 1`

`B.x = 2` creates a new class variable on B. C still reads from A.

---

### Q28. 🟡 What is the output?

```python
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        super().__init__()
        self.x = 2

b = B()
print(b.x)
```

**Answer:** `2` — B's `__init__` runs after A's, overwriting x.

---

### Q29. 🔴 What is the output?

```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        namespace['greeting'] = f"Hello from {name}"
        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=Meta):
    pass

print(MyClass.greeting)
```

**Answer:** `Hello from MyClass` — Metaclass adds attribute during class creation.

---

### Q30. 🟡 Explain method chaining.

**Answer:**
```python
class QueryBuilder:
    def __init__(self):
        self._table = ""
        self._conditions = []
        self._limit = None
    
    def table(self, name):
        self._table = name
        return self           # Return self for chaining
    
    def where(self, condition):
        self._conditions.append(condition)
        return self
    
    def limit(self, n):
        self._limit = n
        return self
    
    def build(self):
        query = f"SELECT * FROM {self._table}"
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

# Method chaining
query = (QueryBuilder()
    .table("users")
    .where("age > 18")
    .where("active = true")
    .limit(10)
    .build())

print(query)
# SELECT * FROM users WHERE age > 18 AND active = true LIMIT 10
```

---

## 🔹 Section 10: Mixins & Composition

### Q31. 🟡 What is a Mixin? How is it different from regular inheritance?

**Answer:**
A Mixin is a class that provides methods to other classes without being a standalone parent.

```python
class JSONMixin:
    """Adds JSON serialization to any class"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LogMixin:
    """Adds logging to any class"""
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class User(JSONMixin, LogMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

u = User("Sid", 25)
print(u.to_json())  # {"name": "Sid", "age": 25}
u.log("Created")     # [User] Created
```

**Rules:**
- Mixins don't have `__init__`
- Mixins provide behavior, not state
- Name ends with `Mixin` (convention)

---

### Q32. 🟡 Composition vs Inheritance — when to use which?

**Answer:**
```python
# Inheritance = "is-a" relationship
class Animal:
    def breathe(self): ...

class Dog(Animal):  # Dog IS-A Animal
    pass

# Composition = "has-a" relationship
class Engine:
    def start(self): return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()  # Car HAS-AN Engine
    
    def start(self):
        return self.engine.start()
```

| | Inheritance | Composition |
|-|-------------|-------------|
| Relationship | is-a | has-a |
| Coupling | Tight | Loose |
| Flexibility | Less | More |
| Reusability | Through hierarchy | Through components |
| **Prefer** | When truly is-a | **Most other cases** |

**Rule of thumb:** "Favor composition over inheritance."

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | 4 pillars of OOP? | Encapsulation, Abstraction, Inheritance, Polymorphism |
| 2 | `self` purpose? | Reference to current instance |
| 3 | `__init__` vs `__new__`? | Initialize vs Create |
| 4 | True private in Python? | No — name mangling only (`__attr`) |
| 5 | `@classmethod` gets? | `cls` (the class itself) |
| 6 | `@staticmethod` gets? | Nothing (utility function) |
| 7 | MRO algorithm? | C3 Linearization |
| 8 | `isinstance()` vs `type()`? | `isinstance` checks inheritance chain |
| 9 | What is `__slots__`? | Fixed attributes, saves memory |
| 10 | SOLID — S? | Single Responsibility Principle |

---

*Next: [04_Functions_Decorators.md](04_Functions_Decorators.md)*
