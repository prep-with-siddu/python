# 07 — Database & ORM — Interview Questions

> **50+ questions covering SQL, PostgreSQL, SQLAlchemy, Redis, MongoDB, migrations**

---

## 🔹 Section 1: SQL Fundamentals

### Q1. 🟢 What is the difference between SQL and NoSQL?

**Answer:**

| Feature | SQL (Relational) | NoSQL (Non-Relational) |
|---------|------------------|------------------------|
| Structure | Tables with rows & columns | Documents, key-value, graph |
| Schema | Fixed schema | Flexible/dynamic schema |
| Scaling | Vertical (bigger server) | Horizontal (more servers) |
| ACID | ✅ Strong | Varies (eventual consistency) |
| Joins | ✅ Powerful | ❌ Limited |
| Examples | PostgreSQL, MySQL | MongoDB, Redis, Cassandra |
| Best for | Complex relationships | High traffic, flexible data |

---

### Q2. 🟢 What is ACID? Why is it important?

**Answer:**

| Property | Meaning | Example |
|----------|---------|---------|
| **Atomicity** | All or nothing | Bank transfer: debit AND credit both succeed or both fail |
| **Consistency** | Valid state transitions | Balance can't go negative if rule exists |
| **Isolation** | Transactions don't interfere | Two users withdraw simultaneously |
| **Durability** | Committed data survives crashes | After commit, data is on disk |

```sql
-- Atomicity example
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Both succeed or both fail
```

---

### Q3. 🟢 What are JOINs? Explain each type.

**Answer:**
```sql
-- Sample tables:
-- users: id, name
-- orders: id, user_id, amount

-- INNER JOIN — only matching rows
SELECT u.name, o.amount
FROM users u INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN — all left rows + matching right
SELECT u.name, o.amount
FROM users u LEFT JOIN orders o ON u.id = o.user_id;
-- Users without orders get NULL for amount

-- RIGHT JOIN — all right rows + matching left
SELECT u.name, o.amount
FROM users u RIGHT JOIN orders o ON u.id = o.user_id;

-- FULL OUTER JOIN — all rows from both
SELECT u.name, o.amount
FROM users u FULL OUTER JOIN orders o ON u.id = o.user_id;

-- CROSS JOIN — cartesian product (all combinations)
SELECT u.name, p.product_name
FROM users u CROSS JOIN products p;
```

---

### Q4. 🟡 What is indexing? When should you create an index?

**Answer:**
An index is a data structure (B-tree, hash) that speeds up data retrieval.

```sql
-- Create index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Unique index
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**When to index:**
- ✅ Columns in WHERE/JOIN/ORDER BY
- ✅ Foreign keys
- ✅ Columns with high cardinality (many unique values)

**When NOT to index:**
- ❌ Small tables
- ❌ Columns that rarely appear in queries
- ❌ Columns with frequent writes (index maintenance cost)

**Downside:** Indexes slow down INSERT/UPDATE/DELETE and use disk space.

---

### Q5. 🟡 What is the difference between `WHERE` and `HAVING`?

**Answer:**
```sql
-- WHERE — filters rows BEFORE grouping
SELECT department, AVG(salary) as avg_salary
FROM employees
WHERE salary > 30000        -- Filter individual rows first
GROUP BY department;

-- HAVING — filters groups AFTER grouping
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;  -- Filter on aggregate result
```

| | WHERE | HAVING |
|-|-------|--------|
| Filters | Individual rows | Groups |
| Timing | Before GROUP BY | After GROUP BY |
| Aggregates | ❌ Cannot use | ✅ Can use |

---

### Q6. 🟡 Explain SQL query execution order.

**Answer:**
```
Written order:    SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
Execution order:  FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

```sql
SELECT department, COUNT(*) as cnt    -- 5
FROM employees                         -- 1
WHERE salary > 30000                   -- 2
GROUP BY department                    -- 3
HAVING COUNT(*) > 5                    -- 4
ORDER BY cnt DESC                      -- 6
LIMIT 10;                              -- 7
```

---

### Q7. 🟡 What is normalization? Explain 1NF, 2NF, 3NF.

**Answer:**

**1NF (First Normal Form):**
- Each column has atomic (single) values
- No repeating groups
```
❌ name: "Sid", skills: "Python, Django, Flask"
✅ Separate skills table with one skill per row
```

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependency (all non-key columns depend on entire primary key)
```
❌ (student_id, course_id) → student_name (depends only on student_id)
✅ Move student_name to students table
```

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependency (non-key depends on another non-key)
```
❌ employee_id → department_id → department_name
✅ Move department_name to departments table
```

---

### Q8. 🟡 What is the N+1 query problem?

**Answer:**
Fetching N related records with N+1 separate queries instead of 1 or 2.

```python
# ❌ N+1 problem (1 query for users + N queries for orders)
users = User.query.all()           # 1 query
for user in users:
    orders = user.orders           # N queries (one per user!)

# ✅ Fix: Eager loading
# SQLAlchemy
users = User.query.options(joinedload(User.orders)).all()  # 1 query

# Django
users = User.objects.prefetch_related('orders').all()       # 2 queries

# Raw SQL — JOIN
SELECT u.*, o.* FROM users u LEFT JOIN orders o ON u.id = o.user_id;
```

---

## 🔹 Section 2: PostgreSQL Specific

### Q9. 🟡 Why PostgreSQL over MySQL for backend?

**Answer:**

| Feature | PostgreSQL | MySQL |
|---------|-----------|-------|
| ACID compliance | ✅ Full | Depends on engine |
| JSON support | ✅ `jsonb` (indexed) | ✅ `JSON` (limited) |
| Full-text search | ✅ Built-in | ✅ Built-in |
| Array columns | ✅ | ❌ |
| CTEs (WITH) | ✅ | ✅ (MySQL 8+) |
| Window functions | ✅ | ✅ (MySQL 8+) |
| Concurrent writes | ✅ MVCC | Row-level locking |
| Extensions | ✅ PostGIS, pg_trgm | Limited |

---

### Q10. 🟡 What are window functions?

**Answer:**
```sql
-- Window functions perform calculations across rows related to current row
-- WITHOUT collapsing rows (unlike GROUP BY)

-- ROW_NUMBER
SELECT name, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- RANK (with gaps for ties)
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- Partition by department
SELECT name, department, salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as diff_from_avg
FROM employees;

-- Running total
SELECT date, amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;
```

---

### Q11. 🟡 What are transactions and isolation levels?

**Answer:**

| Level | Dirty Read | Non-repeatable Read | Phantom Read |
|-------|-----------|--------------------|----|
| READ UNCOMMITTED | ✅ Possible | ✅ Possible | ✅ Possible |
| READ COMMITTED | ❌ | ✅ Possible | ✅ Possible |
| REPEATABLE READ | ❌ | ❌ | ✅ Possible |
| SERIALIZABLE | ❌ | ❌ | ❌ |

```sql
-- PostgreSQL default: READ COMMITTED
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- operations
COMMIT;
```

```python
# SQLAlchemy
with db.session.begin():
    db.session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
    # operations
```

---

## 🔹 Section 3: SQLAlchemy ORM

### Q12. 🟡 What is SQLAlchemy? Core vs ORM?

**Answer:**
SQLAlchemy is Python's most popular database toolkit.

```python
# SQLAlchemy Core — SQL expression language
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://user:pass@localhost/mydb")
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))

# SQLAlchemy ORM — maps classes to tables
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True)
    
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    
    user = relationship("User", back_populates="orders")
```

---

### Q13. 🟡 Explain SQLAlchemy session lifecycle.

**Answer:**
```python
from sqlalchemy.orm import Session

# Session manages objects and their database state
session = Session(engine)

try:
    # 1. Create (add to session)
    user = User(name="Sid", email="sid@example.com")
    session.add(user)
    
    # 2. Query (read)
    user = session.query(User).filter_by(name="Sid").first()
    
    # 3. Update (modify tracked object)
    user.name = "Siddu"
    
    # 4. Delete
    session.delete(user)
    
    # 5. Commit (write to database)
    session.commit()
except Exception:
    session.rollback()  # Undo on error
finally:
    session.close()     # Clean up

# Better: use context manager
with Session(engine) as session:
    with session.begin():
        session.add(User(name="Sid"))
    # Auto-commits or rollbacks
```

---

### Q14. 🟡 What is lazy loading vs eager loading?

**Answer:**
```python
# Lazy loading (default) — queries on access
user = session.query(User).first()
# SELECT * FROM users LIMIT 1
print(user.orders)  # SELECT * FROM orders WHERE user_id = ?  ← extra query!

# Eager loading — joins upfront
from sqlalchemy.orm import joinedload, subqueryload, selectinload

# joinedload — single JOIN query
users = session.query(User).options(joinedload(User.orders)).all()
# SELECT users.*, orders.* FROM users LEFT JOIN orders ON ...

# selectinload — separate SELECT with IN clause
users = session.query(User).options(selectinload(User.orders)).all()
# SELECT * FROM users
# SELECT * FROM orders WHERE user_id IN (1, 2, 3, ...)

# subqueryload — subquery
users = session.query(User).options(subqueryload(User.orders)).all()
```

| Strategy | Queries | Best For |
|----------|---------|----------|
| Lazy | N+1 | Single object access |
| Joined | 1 (JOIN) | One-to-one, small datasets |
| Select-in | 2 | One-to-many |
| Subquery | 2 | Many-to-many |

---

### Q15. 🟡 How do you handle database migrations?

**Answer:**
```bash
# Alembic — migration tool for SQLAlchemy
pip install alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "add users table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1

# Show history
alembic history
```

```python
# Migration file example
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(), unique=True),
    )

def downgrade():
    op.drop_table('users')
```

**Django:** Uses built-in migrations (`python manage.py makemigrations`, `migrate`).

---

## 🔹 Section 4: Redis

### Q16. 🟡 What is Redis? When to use it?

**Answer:**
Redis = Remote Dictionary Server. In-memory key-value store.

**Use cases:**
- **Caching** — API responses, DB query results
- **Session storage** — User sessions
- **Rate limiting** — API throttling
- **Pub/Sub** — Real-time messaging
- **Queues** — Task queues (Celery backend)
- **Leaderboards** — Sorted sets

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Strings
r.set("user:1:name", "Sid")
r.get("user:1:name")         # b"Sid"
r.setex("session:abc", 3600, "user_data")  # Expires in 1hr

# Hashes
r.hset("user:1", mapping={"name": "Sid", "age": "25"})
r.hget("user:1", "name")

# Lists (queues)
r.lpush("tasks", "task1")
r.rpop("tasks")

# Sets
r.sadd("tags:1", "python", "django")
r.smembers("tags:1")

# Sorted Sets (leaderboard)
r.zadd("leaderboard", {"Sid": 100, "Raj": 95})
r.zrange("leaderboard", 0, -1, withscores=True)
```

---

### Q17. 🟡 What caching strategies do you know?

**Answer:**

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Cache-aside** | App checks cache first, loads from DB on miss | General purpose |
| **Write-through** | Write to cache and DB together | Strong consistency |
| **Write-behind** | Write to cache, async write to DB | High write throughput |
| **Read-through** | Cache loads from DB on miss | Similar to cache-aside |

```python
# Cache-aside pattern (most common)
def get_user(user_id):
    # 1. Check cache
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # 2. Cache miss — query DB
    user = db.query(User).get(user_id)
    
    # 3. Store in cache
    redis.setex(f"user:{user_id}", 300, json.dumps(user.to_dict()))
    
    return user.to_dict()

# Cache invalidation
def update_user(user_id, data):
    db.query(User).filter_by(id=user_id).update(data)
    db.commit()
    redis.delete(f"user:{user_id}")  # Invalidate cache
```

---

### Q18. 🟡 What is cache invalidation? Why is it hard?

**Answer:**
> "There are only two hard things in CS: cache invalidation and naming things." — Phil Karlton

**Strategies:**
```python
# 1. TTL (Time-To-Live) — simplest
redis.setex("key", 300, "value")  # Auto-expires in 5 min

# 2. Event-driven invalidation
def update_user(user_id, data):
    db.update(user_id, data)
    redis.delete(f"user:{user_id}")     # Delete specific
    redis.delete(f"user_list")           # Delete related caches

# 3. Version-based
redis.set(f"user:{user_id}:v2", data)  # New version key

# 4. Pattern-based deletion
# redis doesn't support wildcard delete natively
keys = redis.keys("user:*")  # ⚠️ Don't use in production!
# Use SCAN instead
for key in redis.scan_iter("user:*"):
    redis.delete(key)
```

---

## 🔹 Section 5: MongoDB

### Q19. 🟡 When would you use MongoDB over PostgreSQL?

**Answer:**

| Use MongoDB When | Use PostgreSQL When |
|-----------------|---------------------|
| Schema changes frequently | Schema is stable |
| Document-oriented data | Relational data |
| High write throughput | Complex queries/joins |
| Horizontal scaling needed | ACID required |
| Prototyping | Financial data |
| Log/event storage | Reporting/analytics |

```python
# PyMongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["myapp"]
collection = db["users"]

# Insert
collection.insert_one({"name": "Sid", "age": 25, "skills": ["Python"]})

# Find
user = collection.find_one({"name": "Sid"})
users = collection.find({"age": {"$gte": 18}})

# Update
collection.update_one({"name": "Sid"}, {"$set": {"age": 26}})

# Aggregation
pipeline = [
    {"$match": {"age": {"$gte": 18}}},
    {"$group": {"_id": "$city", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = collection.aggregate(pipeline)
```

---

## 🔹 Section 6: Database Design

### Q20. 🟡 How do you design a database for a blog platform?

**Answer:**
```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Posts
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, published
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tags (many-to-many)
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Comments
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    parent_id INTEGER REFERENCES comments(id),  -- Nested comments
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_comments_post ON comments(post_id);
```

---

### Q21. 🟡 What is connection pooling? Why is it important?

**Answer:**
Connection pooling reuses database connections instead of creating new ones.

```python
# SQLAlchemy connection pool
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/mydb",
    pool_size=10,          # Maintain 10 connections
    max_overflow=20,       # Allow up to 20 extra
    pool_timeout=30,       # Wait 30s for connection
    pool_recycle=1800,     # Recycle connections after 30min
    pool_pre_ping=True,    # Check if connection is alive
)
```

**Why important:**
- Creating a DB connection is expensive (~50-100ms)
- Pool reuses connections (~0ms)
- Controls max concurrent connections
- Prevents database overload

---

### Q22. 🟡 What are database deadlocks? How to prevent them?

**Answer:**
Deadlock: Two transactions wait for each other's locks.

```
Transaction A: Lock row 1 → wants row 2
Transaction B: Lock row 2 → wants row 1
→ DEADLOCK!
```

**Prevention:**
```python
# 1. Always lock in the same order
# Always lock user first, then order
def transfer(from_id, to_id, amount):
    low, high = sorted([from_id, to_id])
    lock(low)
    lock(high)

# 2. Use timeouts
session.execute(text("SET lock_timeout = '5s'"))

# 3. Keep transactions short
with session.begin():
    # Do everything quickly
    pass

# 4. Use optimistic locking
class Product(Base):
    version = Column(Integer, default=0)

def update_product(product_id, data):
    product = session.query(Product).get(product_id)
    session.query(Product).filter_by(
        id=product_id, version=product.version
    ).update({**data, "version": product.version + 1})
```

---

### Q23. 🟡 Write a pagination query.

**Answer:**
```python
# Offset-based pagination (simple but slow for large datasets)
def get_users_offset(page=1, per_page=20):
    offset = (page - 1) * per_page
    return session.query(User)\
        .order_by(User.id)\
        .offset(offset)\
        .limit(per_page)\
        .all()

# Cursor-based pagination (efficient for large datasets)
def get_users_cursor(last_id=0, per_page=20):
    return session.query(User)\
        .filter(User.id > last_id)\
        .order_by(User.id)\
        .limit(per_page)\
        .all()
```

| | Offset-based | Cursor-based |
|-|-------------|--------------|
| Speed | Slow on large offsets | Constant time |
| Jump pages | ✅ | ❌ |
| Real-time data | May skip/duplicate | Consistent |
| Best for | Small datasets | Large datasets, infinite scroll |

---

## 🔹 Section 7: Practical Questions

### Q24. 🟡 How do you prevent SQL injection?

**Answer:**
```python
# ❌ NEVER — string concatenation
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# Input: "'; DROP TABLE users; --"

# ✅ Parameterized queries
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))

# ✅ SQLAlchemy ORM (auto-parameterized)
user = session.query(User).filter_by(name=user_input).first()

# ✅ SQLAlchemy Core
from sqlalchemy import text
result = session.execute(text("SELECT * FROM users WHERE name = :name"), {"name": user_input})
```

---

### Q25. 🟡 What is database sharding?

**Answer:**
Splitting database across multiple servers (horizontal partitioning).

```
Users 1-1M     → Shard 1
Users 1M-2M    → Shard 2
Users 2M-3M    → Shard 3
```

**Sharding strategies:**
| Strategy | Method | Pros | Cons |
|----------|--------|------|------|
| Range | ID ranges | Simple | Hot spots |
| Hash | hash(key) % N | Even distribution | Hard to add shards |
| Geographic | By region | Low latency | Uneven load |

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | ACID? | Atomicity, Consistency, Isolation, Durability |
| 2 | N+1 problem? | N extra queries for N related records |
| 3 | Fix N+1? | Eager loading (joinedload, prefetch_related) |
| 4 | SQL injection prevention? | Parameterized queries |
| 5 | Index tradeoff? | Faster reads, slower writes |
| 6 | Redis use case? | Caching, sessions, rate limiting |
| 7 | Connection pooling? | Reuse DB connections for performance |
| 8 | Offset vs cursor pagination? | Cursor is faster for large datasets |
| 9 | Normalization purpose? | Reduce data redundancy |
| 10 | When MongoDB over Postgres? | Flexible schema, high write throughput |

---

*Next: [08_REST_API_Frameworks.md](08_REST_API_Frameworks.md)*
