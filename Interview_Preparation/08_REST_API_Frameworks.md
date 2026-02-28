# 08 — REST API & Web Frameworks — Interview Questions

> **55+ questions covering Django, Flask, FastAPI, REST principles, auth, security**

---

## 🔹 Section 1: REST Fundamentals

### Q1. 🟢 What is REST? What are its principles?

**Answer:**
REST = Representational State Transfer. Architectural style for web APIs.

**6 Constraints:**
1. **Client-Server** — Separate UI from data storage
2. **Stateless** — Each request contains all info needed
3. **Cacheable** — Responses can be cached
4. **Uniform Interface** — Consistent URL structure
5. **Layered System** — Client doesn't know if talking to server or intermediary
6. **Code on Demand** (optional) — Server can send executable code

---

### Q2. 🟢 What are HTTP methods? When to use each?

**Answer:**

| Method | Purpose | Idempotent | Safe | Body |
|--------|---------|-----------|------|------|
| GET | Retrieve resource | ✅ | ✅ | No |
| POST | Create resource | ❌ | ❌ | Yes |
| PUT | Replace resource | ✅ | ❌ | Yes |
| PATCH | Partial update | ❌ | ❌ | Yes |
| DELETE | Remove resource | ✅ | ❌ | Optional |
| HEAD | Get headers only | ✅ | ✅ | No |
| OPTIONS | Get allowed methods | ✅ | ✅ | No |

**Idempotent** = Same request multiple times → same result.

```
GET    /api/users         → List all users
GET    /api/users/123     → Get user 123
POST   /api/users         → Create new user
PUT    /api/users/123     → Replace user 123
PATCH  /api/users/123     → Update user 123 partially
DELETE /api/users/123     → Delete user 123
```

---

### Q3. 🟢 What are HTTP status codes?

**Answer:**

| Range | Category | Common Codes |
|-------|----------|-------------|
| 1xx | Informational | 100 Continue |
| **2xx** | **Success** | 200 OK, 201 Created, 204 No Content |
| **3xx** | **Redirection** | 301 Moved, 302 Found, 304 Not Modified |
| **4xx** | **Client Error** | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 409 Conflict, 422 Unprocessable, 429 Too Many Requests |
| **5xx** | **Server Error** | 500 Internal Error, 502 Bad Gateway, 503 Unavailable, 504 Timeout |

**Backend tip:**
- 401 = Not authenticated ("Who are you?")
- 403 = Not authorized ("You can't do this")
- 422 = Validation error (FastAPI default)

---

### Q4. 🟡 How should you design RESTful URLs?

**Answer:**
```
✅ Good REST URLs:
GET    /api/v1/users                  → List users
GET    /api/v1/users/123              → Get user
POST   /api/v1/users                  → Create user
PUT    /api/v1/users/123              → Update user
DELETE /api/v1/users/123              → Delete user
GET    /api/v1/users/123/orders       → User's orders
GET    /api/v1/users/123/orders/456   → Specific order
GET    /api/v1/users?page=1&limit=20  → Pagination
GET    /api/v1/users?sort=name&order=asc → Sorting

❌ Bad REST URLs:
GET    /api/getUser/123
POST   /api/deleteUser/123
GET    /api/user_list
POST   /api/createNewUser
```

**Rules:**
- Use nouns, not verbs
- Use plural (`/users` not `/user`)
- Use kebab-case (`/user-profiles`)
- Version your API (`/v1/`, `/v2/`)
- Use query params for filtering/sorting

---

### Q5. 🟡 What is the difference between authentication and authorization?

**Answer:**

| | Authentication (AuthN) | Authorization (AuthZ) |
|-|----------------------|---------------------|
| Question | "Who are you?" | "What can you do?" |
| When | Login | After login, each request |
| HTTP code | 401 Unauthorized | 403 Forbidden |
| Example | Username/password | Role-based permissions |

---

### Q6. 🟡 What is JWT? How does it work?

**Answer:**
JWT = JSON Web Token. Stateless authentication token.

```
Structure: HEADER.PAYLOAD.SIGNATURE

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"user_id": 123, "role": "admin", "exp": 1709136000}
Signature: HMACSHA256(base64(header) + "." + base64(payload), SECRET_KEY)
```

```python
# PyJWT
import jwt
from datetime import datetime, timedelta

SECRET = "your-secret-key"

# Create token
def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

# Verify token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token")
```

**JWT flow:**
```
1. Client sends credentials → Server verifies → Returns JWT
2. Client stores JWT (localStorage/cookie)
3. Client sends JWT in header: Authorization: Bearer <token>
4. Server verifies JWT signature → grants/denies access
```

---

### Q7. 🟡 JWT vs Session-based authentication?

**Answer:**

| Feature | JWT | Session |
|---------|-----|---------|
| Storage | Client (token) | Server (session store) |
| Stateless | ✅ | ❌ |
| Scalable | ✅ (no server state) | Need shared session store |
| Revocation | ❌ Hard | ✅ Easy (delete session) |
| Size | Larger (payload in token) | Small (session ID) |
| Best for | APIs, microservices | Traditional web apps |

---

## 🔹 Section 2: Django

### Q8. 🟡 What is Django? Explain its architecture.

**Answer:**
Django follows **MVT (Model-View-Template)** pattern.

```
Client Request → URL Router → View → Model (DB) → Template → Response

Model:    Database layer (ORM)
View:     Business logic (handles request/response)
Template: HTML rendering (presentation)
```

**Key features:**
- Built-in admin panel
- ORM (powerful, batteries-included)
- Authentication system
- Middleware support
- Form handling
- Security features (CSRF, XSS protection)

---

### Q9. 🟡 Explain Django request/response lifecycle.

**Answer:**
```
1. WSGI Server receives request
2. Django creates HttpRequest object
3. Middleware (request phase) — top to bottom
4. URL resolver matches URL pattern
5. View function/class called
6. View processes request (DB queries, business logic)
7. View returns HttpResponse
8. Middleware (response phase) — bottom to top
9. Response sent to client
```

---

### Q10. 🟡 What is Django middleware?

**Answer:**
Middleware processes requests/responses globally.

```python
# Custom middleware
class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        import time
        start = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start
        response['X-Request-Duration'] = f"{duration:.4f}s"
        return response

# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'myapp.middleware.RequestTimingMiddleware',  # Custom
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

---

### Q11. 🟡 Django ORM: `select_related` vs `prefetch_related`?

**Answer:**
```python
# select_related — SQL JOIN (ForeignKey, OneToOne)
# Single query with JOIN
users = User.objects.select_related('profile').all()
# SELECT users.*, profiles.* FROM users JOIN profiles ON ...

# prefetch_related — Separate queries (ManyToMany, reverse FK)
# 2 queries
users = User.objects.prefetch_related('orders').all()
# SELECT * FROM users
# SELECT * FROM orders WHERE user_id IN (1, 2, 3, ...)
```

| | `select_related` | `prefetch_related` |
|-|-----------------|-------------------|
| SQL | JOIN | Separate SELECT + IN |
| Relations | ForeignKey, OneToOne | ManyToMany, reverse FK |
| Queries | 1 | 2 |
| Best for | Single related object | Multiple related objects |

---

### Q12. 🟡 What is Django REST Framework (DRF)?

**Answer:**
DRF extends Django for building RESTful APIs.

```python
# serializers.py
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

# views.py
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = router.urls
```

**DRF features:**
- Serializers (validation + serialization)
- ViewSets (CRUD in one class)
- Authentication (Token, JWT, Session)
- Permissions
- Throttling
- Pagination
- Browsable API

---

## 🔹 Section 3: Flask

### Q13. 🟡 What is Flask? How is it different from Django?

**Answer:**

| Feature | Django | Flask |
|---------|--------|-------|
| Type | Full-stack "batteries included" | Micro-framework |
| ORM | Built-in | None (use SQLAlchemy) |
| Admin | Built-in | None |
| Template | Django templates | Jinja2 |
| Learning curve | Steeper | Easier |
| Flexibility | Opinionated | Choose your own |
| Best for | Large apps | Small-medium, microservices |

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return jsonify([u.to_dict() for u in users.items])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404
```

---

### Q14. 🟡 What is Flask Blueprint?

**Answer:**
Blueprints organize Flask apps into modular components.

```python
# users/routes.py
from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/')
def list_users():
    return jsonify(users)

@users_bp.route('/<int:id>')
def get_user(id):
    return jsonify(user)

# app.py
from users.routes import users_bp
from orders.routes import orders_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(orders_bp)
```

---

## 🔹 Section 4: FastAPI

### Q15. 🟡 What is FastAPI? Why is it gaining popularity?

**Answer:**
FastAPI is a modern, async Python web framework.

**Key features:**
- **Async support** (built on Starlette + Uvicorn)
- **Automatic API docs** (Swagger UI + ReDoc)
- **Type hints validation** (Pydantic)
- **Performance** — comparable to Node.js/Go
- **Easy to learn** — minimal boilerplate

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    return await db.create_user(user.dict())
```

---

### Q16. 🟡 Django vs Flask vs FastAPI — when to use each?

**Answer:**

| | Django | Flask | FastAPI |
|-|--------|-------|---------|
| Type | Full-stack | Micro | Async micro |
| Async | Limited | No (ext.) | ✅ Native |
| Performance | Good | Good | Excellent |
| API Docs | Manual | Manual | ✅ Auto (Swagger) |
| Validation | Forms/DRF | Manual | ✅ Pydantic |
| Learning | Steep | Easy | Easy |
| Best for | Full web apps | Small/medium APIs | High-perf APIs |
| ORM | Built-in | SQLAlchemy | SQLAlchemy/Tortoise |
| Admin | ✅ Built-in | ❌ | ❌ |

**Choose:**
- **Django** → Full web app with admin, auth, templates
- **Flask** → Simple API, microservices, maximum flexibility
- **FastAPI** → High-performance async API, modern Python

---

### Q17. 🟡 What is Pydantic? Why is it important?

**Answer:**
Pydantic provides data validation using Python type hints.

```python
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    role: str = "user"
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()

# Auto-validation
user = UserCreate(name="sid", email="sid@example.com", age=25)
print(user.name)  # "Sid" (title-cased by validator)

# Invalid data raises ValidationError
try:
    UserCreate(name="", email="bad", age=-1)
except ValidationError as e:
    print(e.errors())
```

---

## 🔹 Section 5: API Security

### Q18. 🟡 What is CORS? How to handle it?

**Answer:**
CORS = Cross-Origin Resource Sharing. Browser security that blocks requests from different origins.

```python
# Flask
from flask_cors import CORS
CORS(app, origins=["https://myapp.com"])

# FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Django
# pip install django-cors-headers
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOWED_ORIGINS = ["https://myapp.com"]
```

---

### Q19. 🟡 What is CSRF? How to prevent it?

**Answer:**
CSRF = Cross-Site Request Forgery. Attacker tricks user into submitting a request.

```python
# Django — CSRF protection built-in
MIDDLEWARE = ['django.middleware.csrf.CsrfViewMiddleware']

# Template
<form method="POST">
    {% csrf_token %}
    <input type="text" name="amount">
</form>

# For APIs (usually stateless = no CSRF needed)
# JWT-based auth doesn't need CSRF protection
# Session-based auth DOES need CSRF tokens
```

---

### Q20. 🟡 What are common API security best practices?

**Answer:**
```python
# 1. Input validation
from pydantic import BaseModel, constr
class UserInput(BaseModel):
    name: constr(min_length=1, max_length=100)

# 2. Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/users")
@limiter.limit("100/minute")
async def get_users():
    pass

# 3. SQL injection prevention — use ORM/parameterized queries

# 4. Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])
hashed = pwd_context.hash("password123")
pwd_context.verify("password123", hashed)

# 5. HTTPS only
# 6. API key / JWT authentication
# 7. Request size limits
# 8. Logging & monitoring
# 9. CORS configuration
# 10. Input sanitization
```

---

### Q21. 🟡 How do you implement rate limiting?

**Answer:**
```python
# Token Bucket algorithm
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        # Clean old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id]
            if t > now - self.window
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        self.requests[client_id].append(now)
        return True

# Redis-based (production)
def is_rate_limited(redis, user_id, max_requests=100, window=60):
    key = f"rate:{user_id}"
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, window)
    return current > max_requests
```

---

## 🔹 Section 6: API Design Patterns

### Q22. 🟡 What is API versioning? What strategies exist?

**Answer:**
```python
# 1. URL versioning (most common)
GET /api/v1/users
GET /api/v2/users

# 2. Header versioning
GET /api/users
Accept: application/vnd.myapp.v2+json

# 3. Query parameter
GET /api/users?version=2
```

---

### Q23. 🟡 How do you handle file uploads?

**Answer:**
```python
# FastAPI
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Invalid file type")
    if file.size > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(400, "File too large")
    
    # Save
    contents = await file.read()
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(contents)
    
    return {"filename": file.filename, "size": len(contents)}

# Production: Use cloud storage (S3, GCS)
import boto3
s3 = boto3.client('s3')
s3.upload_fileobj(file.file, 'my-bucket', f'uploads/{file.filename}')
```

---

### Q24. 🟡 What is WebSocket? When to use it over REST?

**Answer:**
```python
# FastAPI WebSocket
from fastapi import WebSocket

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

| Feature | REST | WebSocket |
|---------|------|-----------|
| Connection | Request-response | Persistent |
| Direction | Client → Server | Bidirectional |
| Overhead | HTTP headers each time | Minimal after handshake |
| Use case | CRUD operations | Real-time (chat, live data) |

---

### Q25. 🟡 What is GraphQL vs REST?

**Answer:**

| Feature | REST | GraphQL |
|---------|------|---------|
| Endpoints | Multiple (`/users`, `/orders`) | Single (`/graphql`) |
| Data fetching | Fixed structure | Client specifies fields |
| Over-fetching | Common | ❌ Solved |
| Under-fetching | Common (N+1 API calls) | ❌ Solved |
| Caching | Easy (HTTP caching) | Complex |
| Learning curve | Lower | Higher |

```python
# GraphQL query example
{
  user(id: 123) {
    name
    email
    orders {
      id
      amount
    }
  }
}
# Returns exactly what you asked for — no more, no less
```

---

## 🔹 Section 7: WSGI & ASGI

### Q26. 🟡 What is WSGI? What is ASGI?

**Answer:**

| | WSGI | ASGI |
|-|------|------|
| Full name | Web Server Gateway Interface | Async Server Gateway Interface |
| Type | Synchronous | Asynchronous |
| Protocol | HTTP only | HTTP + WebSocket + HTTP/2 |
| Frameworks | Django, Flask | FastAPI, Django (3.0+) |
| Servers | Gunicorn, uWSGI | Uvicorn, Daphne, Hypercorn |

```python
# WSGI app (simplest form)
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello World']

# ASGI app
async def app(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/plain']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello World',
    })
```

---

### Q27. 🟡 What is Gunicorn? How to configure it?

**Answer:**
```bash
# Gunicorn = Green Unicorn — WSGI HTTP server for production

# Basic
gunicorn app:app --workers 4 --bind 0.0.0.0:8000

# With Uvicorn workers (for async frameworks)
gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 4

# Production config
gunicorn app:app \
    --workers 4 \           # 2 * CPU cores + 1
    --threads 2 \           # Threads per worker
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --max-requests 1000 \   # Restart worker after N requests
    --max-requests-jitter 50
```

---

## 🔹 Section 8: Background Tasks

### Q28. 🟡 What is Celery? When to use it?

**Answer:**
Celery is a distributed task queue for background processing.

```python
# celery_app.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def send_email(to, subject, body):
    # Long-running task
    email_service.send(to, subject, body)
    return "sent"

# Usage (non-blocking)
send_email.delay("sid@example.com", "Welcome", "Hello!")

# With options
send_email.apply_async(
    args=["sid@example.com", "Welcome", "Hello!"],
    countdown=60,  # Delay 60 seconds
    retry=True,
    retry_policy={'max_retries': 3}
)
```

**Use cases:**
- Sending emails/notifications
- Image/video processing
- Data exports (CSV, PDF)
- Periodic tasks (cron-like)
- Third-party API calls

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | REST constraint? | Stateless client-server |
| 2 | 401 vs 403? | Not authenticated vs Not authorized |
| 3 | JWT stored where? | Client (token contains payload) |
| 4 | Django pattern? | MVT (Model-View-Template) |
| 5 | Flask vs Django? | Micro vs Full-stack |
| 6 | FastAPI advantage? | Async + auto docs + Pydantic |
| 7 | CORS purpose? | Browser security for cross-origin |
| 8 | WSGI vs ASGI? | Sync vs Async server interface |
| 9 | Celery purpose? | Background task processing |
| 10 | Rate limiting? | Prevent API abuse (X requests/time) |

---

*Next: [09_Testing.md](09_Testing.md)*
