# 10 — System Design & Architecture — Interview Questions

> **45+ questions covering scalability, caching, message queues, microservices, design patterns, load balancing**

---

## 🔹 Section 1: System Design Fundamentals

### Q1. 🟢 What is scalability? Horizontal vs Vertical?

**Answer:**

| | Vertical (Scale Up) | Horizontal (Scale Out) |
|-|--------------------|-----------------------|
| How | Bigger machine (more RAM, CPU) | More machines |
| Cost | Expensive, has limits | Cost-effective |
| Downtime | Requires restart | Zero downtime |
| Complexity | Simple | Need load balancer |
| Example | Upgrade DB server | Add more app servers |

```
Vertical:  🖥️ → 🖥️🖥️ (bigger)
Horizontal: 🖥️ → 🖥️ 🖥️ 🖥️ (more)
```

---

### Q2. 🟢 What is a load balancer?

**Answer:**
Distributes incoming traffic across multiple servers.

```
                    ┌── Server 1
Client → LB ──────├── Server 2
                    └── Server 3

Algorithms:
- Round Robin       → 1, 2, 3, 1, 2, 3...
- Weighted RR       → More traffic to powerful servers
- Least Connections → Route to least busy server
- IP Hash           → Same client → same server (sticky sessions)
- Random            → Random selection
```

**Tools:** Nginx, HAProxy, AWS ALB/ELB, Traefik

---

### Q3. 🟡 What is a CDN?

**Answer:**
CDN = Content Delivery Network. Caches static content at edge locations close to users.

```
Without CDN:  User (India) → Server (US)  = 300ms
With CDN:     User (India) → CDN (India)  = 20ms
```

**What to put on CDN:** Images, CSS, JS, videos, static HTML
**Providers:** CloudFront, Cloudflare, Akamai, Fastly

---

### Q4. 🟡 What is CAP theorem?

**Answer:**
In a distributed system, you can only guarantee **2 of 3**:

| | Description |
|-|-------------|
| **C** — Consistency | All nodes see same data at same time |
| **A** — Availability | System always responds |
| **P** — Partition Tolerance | System works despite network failures |

**P is mandatory** in distributed systems, so real choice is **CP vs AP**:
- **CP** (Consistency + Partition) → MongoDB (configurable), HBase
- **AP** (Availability + Partition) → Cassandra, DynamoDB, DNS

---

### Q5. 🟡 What is database sharding?

**Answer:**
Splitting data across multiple database instances.

```python
# Sharding strategies

# 1. Range-based
def get_shard(user_id):
    if user_id < 1_000_000:
        return "shard_1"
    elif user_id < 2_000_000:
        return "shard_2"
    else:
        return "shard_3"

# 2. Hash-based (more uniform)
def get_shard(user_id, num_shards=4):
    return f"shard_{hash(user_id) % num_shards}"

# 3. Geographic
# US users → US shard, EU users → EU shard
```

**Challenges:** Cross-shard queries, rebalancing, joins across shards

---

## 🔹 Section 2: Caching

### Q6. 🟡 What are caching strategies?

**Answer:**

| Strategy | Read/Write | Flow |
|----------|-----------|------|
| **Cache-Aside** | Read | App checks cache → miss → query DB → update cache |
| **Read-Through** | Read | Cache handles DB read on miss |
| **Write-Through** | Write | Write to cache + DB simultaneously |
| **Write-Behind** | Write | Write to cache → async write to DB |
| **Write-Around** | Write | Write to DB only → cache on read |

```python
# Cache-Aside (most common)
import redis

cache = redis.Redis()

def get_user(user_id):
    # Check cache
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Cache miss — query DB
    user = db.query(User).get(user_id)
    
    # Update cache (with TTL)
    cache.setex(f"user:{user_id}", 3600, json.dumps(user.to_dict()))
    return user.to_dict()
```

---

### Q7. 🟡 What is cache invalidation?

**Answer:**
The two hard things in computer science: **cache invalidation** and **naming things**.

```python
# 1. TTL (Time-To-Live) — simplest
cache.setex("key", 300, "value")  # Expires in 5 min

# 2. Event-based invalidation
def update_user(user_id, data):
    db.update(user_id, data)
    cache.delete(f"user:{user_id}")  # Invalidate cache

# 3. Write-through
def update_user(user_id, data):
    db.update(user_id, data)
    cache.set(f"user:{user_id}", json.dumps(data))  # Update cache

# 4. Cache stampede prevention
import hashlib, random

def get_with_jitter(key, ttl=300):
    jitter = random.randint(0, 60)  # Random 0-60s extra
    cache.setex(key, ttl + jitter, value)
```

**Cache stampede:** When many requests hit an expired cache key simultaneously → all go to DB.

---

### Q8. 🟡 Redis vs Memcached?

**Answer:**

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data types | Strings, lists, sets, hashes, sorted sets | Strings only |
| Persistence | ✅ (RDB, AOF) | ❌ |
| Pub/Sub | ✅ | ❌ |
| Clustering | ✅ | ✅ |
| Transactions | ✅ | ❌ |
| Lua scripting | ✅ | ❌ |
| Memory | More features = more overhead | Simpler, efficient |
| Use case | Versatile cache + data store | Simple key-value cache |

---

## 🔹 Section 3: Message Queues

### Q9. 🟡 What is a message queue? Why use one?

**Answer:**
Message queues decouple producers from consumers for async processing.

```
Producer → [Message Queue] → Consumer

Example:
User Signup → [Queue] → Send Welcome Email
                      → Create Default Settings
                      → Notify Admin
```

**Benefits:**
- **Decoupling** — Services don't need to know about each other
- **Async processing** — Don't block user request
- **Load leveling** — Handle traffic spikes
- **Retry** — Failed tasks can be retried
- **Scaling** — Add more consumers independently

**Tools:** RabbitMQ, Apache Kafka, AWS SQS, Redis (basic)

---

### Q10. 🟡 RabbitMQ vs Kafka?

**Answer:**

| Feature | RabbitMQ | Kafka |
|---------|----------|-------|
| Type | Message Broker | Event Streaming Platform |
| Pattern | Push to consumers | Consumers pull |
| Message retention | Until consumed | Configurable time |
| Ordering | Per queue | Per partition |
| Throughput | ~50K msg/sec | ~1M+ msg/sec |
| Best for | Task queues, RPC | Event streaming, logs |
| Replay | ❌ | ✅ (re-read old events) |

---

### Q11. 🟡 What is the Pub/Sub pattern?

**Answer:**
```
Publisher → Topic → Subscriber 1
                 → Subscriber 2
                 → Subscriber 3

# Redis Pub/Sub
import redis
r = redis.Redis()

# Publisher
r.publish('notifications', json.dumps({
    "user_id": 123,
    "message": "Order shipped"
}))

# Subscriber
pubsub = r.pubsub()
pubsub.subscribe('notifications')
for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        process_notification(data)
```

---

## 🔹 Section 4: Microservices

### Q12. 🟡 Monolith vs Microservices?

**Answer:**

| | Monolith | Microservices |
|-|----------|--------------|
| Deployment | All-or-nothing | Independent |
| Scaling | Scale entire app | Scale individual services |
| Tech stack | Single | Different per service |
| Complexity | Simple initially | Complex (networking, etc.) |
| Team size | Small teams | Large teams |
| DB | Shared | DB per service |
| Debugging | Easy (single process) | Hard (distributed tracing) |

```
Monolith:
┌──────────────────────┐
│  Users + Orders +    │
│  Payments + Email    │
│  (single codebase)   │
└──────────────────────┘

Microservices:
┌──────┐ ┌──────┐ ┌────────┐ ┌──────┐
│Users │ │Orders│ │Payments│ │Email │
└──────┘ └──────┘ └────────┘ └──────┘
  DB1      DB2      DB3       Queue
```

---

### Q13. 🟡 How do microservices communicate?

**Answer:**

| Method | Type | Use Case |
|--------|------|----------|
| REST API | Sync | Request-response |
| gRPC | Sync | High-performance, streaming |
| Message Queue | Async | Events, background tasks |
| GraphQL | Sync | Flexible data fetching |

```python
# Sync: Service A calls Service B via REST
import httpx

async def get_user_orders(user_id):
    async with httpx.AsyncClient() as client:
        user = await client.get(f"http://user-service/users/{user_id}")
        orders = await client.get(f"http://order-service/users/{user_id}/orders")
    return {**user.json(), "orders": orders.json()}

# Async: Service A publishes event, Service B consumes
# User service publishes "user_created" event
# Email service consumes it and sends welcome email
```

---

### Q14. 🔴 What is the Circuit Breaker pattern?

**Answer:**
Prevents cascading failures when a service is down.

```python
from enum import Enum
import time

class State(Enum):
    CLOSED = "closed"      # Normal — requests pass through
    OPEN = "open"          # Failing — block requests
    HALF_OPEN = "half_open"  # Testing — allow few requests

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.state = State.CLOSED
        self.failures = 0
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None
    
    def call(self, func, *args):
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = State.HALF_OPEN
            else:
                raise CircuitOpenError("Service unavailable")
        
        try:
            result = func(*args)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failures = 0
        self.state = State.CLOSED
    
    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.threshold:
            self.state = State.OPEN
```

---

### Q15. 🟡 What is an API Gateway?

**Answer:**
Single entry point for all client requests to microservices.

```
Client → API Gateway → User Service
                     → Order Service
                     → Payment Service

Responsibilities:
- Request routing
- Authentication / Authorization
- Rate limiting
- Load balancing
- Caching
- Request/Response transformation
- Logging & monitoring
- SSL termination
```

**Tools:** Kong, AWS API Gateway, Nginx, Traefik

---

## 🔹 Section 5: Design Patterns (Backend)

### Q16. 🟡 What is the Repository pattern?

**Answer:**
Abstracts data access layer from business logic.

```python
# repository.py — Data access
class UserRepository:
    def __init__(self, session):
        self.session = session
    
    def get_by_id(self, user_id: int) -> User:
        return self.session.query(User).get(user_id)
    
    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()
    
    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

# service.py — Business logic
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def register(self, name, email):
        if self.repo.get_by_email(email):
            raise ValueError("Email already exists")
        user = User(name=name, email=email)
        return self.repo.create(user)
```

**Benefits:** Testable (mock repository), swappable DB, single responsibility

---

### Q17. 🟡 What is the Service Layer pattern?

**Answer:**
```python
# Separation of concerns:
# View → Service → Repository → Database

# views.py (thin — just HTTP handling)
@app.post("/api/users")
async def create_user(data: UserCreate):
    user = user_service.register(data.name, data.email)
    return UserResponse.from_orm(user)

# services.py (business logic)
class UserService:
    def register(self, name, email):
        # Validate business rules
        if not is_valid_email(email):
            raise ValidationError("Invalid email")
        
        # Create user
        user = self.repo.create(User(name=name, email=email))
        
        # Side effects
        self.email_service.send_welcome(user.email)
        self.analytics.track("user_registered", user.id)
        
        return user
```

---

### Q18. 🟡 What is Event-Driven Architecture?

**Answer:**
```
                    Event Bus / Message Broker
                    ┌─────────────────────┐
User Signup ──────→ │ "user_created"      │
                    │                     │──→ Email Service (send welcome)
                    │                     │──→ Analytics (track signup)
                    │                     │──→ Notification (notify admin)
                    └─────────────────────┘

Benefits:
- Loose coupling — services don't know about each other
- Easy to add new consumers
- Async processing
- Event sourcing (replay events to rebuild state)
```

---

## 🔹 Section 6: Common System Design Questions

### Q19. 🔴 Design a URL shortener (like bit.ly).

**Answer:**
```
Requirements:
- Generate short URL from long URL
- Redirect short URL to original
- Track click analytics

Components:
┌──────┐    ┌───────────┐    ┌────┐    ┌───────┐
│Client│ →  │API Gateway │ →  │App │ →  │  DB   │
└──────┘    └───────────┘    └────┘    └───────┘
                                ↓
                            ┌──────┐
                            │Cache │ (Redis)
                            └──────┘

API:
POST /api/shorten   {"url": "https://very-long-url.com/..."}
GET  /:code         → 301 Redirect to original URL

Algorithm:
1. Hash the URL → Base62 encode → 7 chars = 3.5T unique URLs
2. Or use auto-increment ID → Base62 encode

DB Schema:
urls (id, short_code, original_url, created_at, expires_at, click_count)

Scaling:
- Cache popular URLs in Redis
- DB read replicas for redirects
- Sharding by short_code hash
```

---

### Q20. 🔴 Design a rate limiter.

**Answer:**
```
Algorithms:
1. Fixed Window    — Count requests per time window (simple)
2. Sliding Window  — More accurate, harder to implement
3. Token Bucket    — Tokens added at fixed rate, consumed per request
4. Leaky Bucket    — Requests processed at fixed rate

Token Bucket (Redis):
```

```python
import time
import redis

class TokenBucket:
    def __init__(self, redis_client, max_tokens=100, refill_rate=10):
        self.redis = redis_client
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate  # tokens per second
    
    def is_allowed(self, key):
        pipe = self.redis.pipeline()
        now = time.time()
        bucket_key = f"ratelimit:{key}"
        
        # Get current state
        data = self.redis.hmget(bucket_key, "tokens", "last_refill")
        tokens = float(data[0] or self.max_tokens)
        last_refill = float(data[1] or now)
        
        # Refill tokens
        elapsed = now - last_refill
        tokens = min(self.max_tokens, tokens + elapsed * self.refill_rate)
        
        if tokens >= 1:
            tokens -= 1
            allowed = True
        else:
            allowed = False
        
        # Save state
        pipe.hmset(bucket_key, {"tokens": tokens, "last_refill": now})
        pipe.expire(bucket_key, 300)
        pipe.execute()
        
        return allowed
```

---

### Q21. 🔴 Design a notification system.

**Answer:**
```
Requirements:
- Multi-channel: Email, SMS, Push, In-app
- User preferences (opt-in/opt-out per channel)
- Template-based messages
- Retry on failure

Architecture:
┌─────────┐    ┌──────────────┐    ┌──────────────────┐
│Trigger  │ →  │Notification  │ →  │  Message Queue    │
│Service  │    │Service       │    │                    │
└─────────┘    └──────────────┘    └──────────────────┘
                                     ↓        ↓        ↓
                                   Email    SMS     Push
                                   Worker   Worker  Worker

Flow:
1. Event triggers notification (order placed, etc.)
2. Notification service checks user preferences
3. Renders template with data
4. Publishes to channel-specific queue
5. Worker processes and sends via provider
6. Retry on failure (exponential backoff)
7. Store delivery status for tracking
```

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | Horizontal vs Vertical? | More machines vs Bigger machine |
| 2 | CAP theorem? | Pick 2: Consistency, Availability, Partition Tolerance |
| 3 | Cache-Aside? | Read cache → miss → DB → update cache |
| 4 | Cache stampede? | Many requests hit expired key simultaneously |
| 5 | RabbitMQ vs Kafka? | Task queue vs Event streaming |
| 6 | Monolith vs Micro? | Single deploy vs Independent services |
| 7 | Circuit Breaker? | Stop calling failing service temporarily |
| 8 | API Gateway? | Single entry point for microservices |
| 9 | Repository pattern? | Abstracts data access from business logic |
| 10 | Sharding? | Split data across multiple DBs |

---

*Next: [11_DevOps_Deployment.md](11_DevOps_Deployment.md)*
