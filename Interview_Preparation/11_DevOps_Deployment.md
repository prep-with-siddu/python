# 11 — DevOps & Deployment — Interview Questions

> **40+ questions covering Docker, CI/CD, Nginx, Gunicorn, monitoring, cloud, Kubernetes**

---

## 🔹 Section 1: Docker

### Q1. 🟢 What is Docker? Why use it?

**Answer:**
Docker packages applications + dependencies into portable containers.

```
Traditional:  "Works on my machine" 😅
Docker:       "Works everywhere"     ✅

Benefits:
- Consistent environment (dev = staging = prod)
- Isolation (no dependency conflicts)
- Lightweight (shares OS kernel, unlike VMs)
- Fast startup (seconds vs minutes for VMs)
- Easy scaling and deployment
```

---

### Q2. 🟢 Docker Image vs Container?

**Answer:**

| | Image | Container |
|-|-------|-----------|
| What | Blueprint/template | Running instance |
| Analogy | Class | Object |
| State | Read-only | Read-write |
| Storage | On disk | In memory |

```bash
# Image = recipe
docker build -t myapp:latest .

# Container = cooked meal
docker run -d --name myapp-1 myapp:latest
docker run -d --name myapp-2 myapp:latest  # Another instance
```

---

### Q3. 🟡 Write a Dockerfile for a Python app.

**Answer:**
```dockerfile
# Use slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user (security)
RUN adduser --disabled-password appuser
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

**Best practices:**
- Use slim/alpine base images
- Copy requirements.txt first (leverage cache)
- Don't run as root
- Use `.dockerignore`
- Multi-stage builds for smaller images

---

### Q4. 🟡 What is Docker Compose?

**Answer:**
Docker Compose manages multi-container applications.

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    restart: always

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A tasks worker --loglevel=info
    depends_on:
      - redis

volumes:
  postgres_data:
```

```bash
docker-compose up -d        # Start all services
docker-compose down          # Stop all
docker-compose logs -f web   # View logs
docker-compose exec web bash # Shell into container
```

---

### Q5. 🟡 What is multi-stage Docker build?

**Answer:**
```dockerfile
# Stage 1: Build
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Production (smaller image)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]

# Result: Smaller final image without build tools
```

---

### Q6. 🟡 Docker networking — how do containers communicate?

**Answer:**
```bash
# Default: bridge network
docker network create mynetwork

docker run -d --name web --network mynetwork myapp
docker run -d --name db --network mynetwork postgres

# web can reach db by hostname: postgresql://db:5432

# Network types:
# bridge  — Default, containers on same host
# host    — Share host's network (no isolation)
# overlay — Multi-host (Docker Swarm / K8s)
# none    — No network
```

---

## 🔹 Section 2: CI/CD

### Q7. 🟡 What is CI/CD?

**Answer:**
```
CI = Continuous Integration
    → Automatically build & test every commit

CD = Continuous Delivery/Deployment
    → Automatically deploy to staging/production

Pipeline:
Code Push → Build → Test → Lint → Deploy Staging → Deploy Prod
   ↓                                    ↓
  Git              Automated         Manual/Auto
```

---

### Q8. 🟡 Write a GitHub Actions CI/CD pipeline.

**Answer:**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 10s
      
      redis:
        image: redis:7
        ports: ["6379:6379"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      
      - name: Lint
        run: flake8 src/ --max-line-length 120
      
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/postgres
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # ssh, docker push, kubectl apply, etc.
```

---

## 🔹 Section 3: Web Server Configuration

### Q9. 🟡 What is Nginx? How is it used?

**Answer:**
Nginx = High-performance reverse proxy, load balancer, and web server.

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name myapp.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name myapp.com;

    ssl_certificate /etc/ssl/certs/myapp.crt;
    ssl_certificate_key /etc/ssl/private/myapp.key;

    # Static files
    location /static/ {
        alias /app/static/;
        expires 30d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Architecture:**
```
Client → Nginx (port 80/443) → Gunicorn (port 8000) → Python App
                ↳ Static files served directly
```

---

### Q10. 🟡 Nginx vs Gunicorn — roles?

**Answer:**

| | Nginx | Gunicorn |
|-|-------|----------|
| Type | Reverse proxy / Web server | WSGI Application server |
| Handles | Static files, SSL, load balancing | Python application |
| Concurrency | Async, event-driven | Process-based (workers) |
| Language | C | Python |

```
Client → Nginx → Gunicorn → Django/Flask
          ↓
      Static files
      SSL termination
      Rate limiting
      Gzip compression
```

---

## 🔹 Section 4: Cloud & Infrastructure

### Q11. 🟡 What is Infrastructure as Code (IaC)?

**Answer:**
Manage infrastructure through code instead of manual setup.

```python
# Terraform example
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  
  tags = {
    Name = "web-server"
  }
}

# Benefits:
# - Version controlled
# - Reproducible
# - Automated
# - Reviewable (PR process)

# Tools: Terraform, Pulumi, CloudFormation, Ansible
```

---

### Q12. 🟡 What AWS services should a Python backend dev know?

**Answer:**

| Service | Purpose |
|---------|---------|
| **EC2** | Virtual servers |
| **RDS** | Managed PostgreSQL/MySQL |
| **S3** | File/object storage |
| **ElastiCache** | Managed Redis/Memcached |
| **SQS** | Message queue |
| **Lambda** | Serverless functions |
| **ECS/EKS** | Container orchestration |
| **CloudWatch** | Monitoring & logging |
| **API Gateway** | API management |
| **Route 53** | DNS |

---

## 🔹 Section 5: Kubernetes Basics

### Q13. 🟡 What is Kubernetes (K8s)?

**Answer:**
Kubernetes orchestrates containerized applications at scale.

```
Key concepts:
- Pod         — Smallest unit (1+ containers)
- Deployment  — Manages pods (replicas, updates)
- Service     — Network endpoint for pods
- Ingress     — External access (HTTP routing)
- ConfigMap   — Configuration data
- Secret      — Sensitive data (passwords, keys)
- Namespace   — Virtual clusters
```

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl scale deployment myapp --replicas=5
kubectl logs myapp-pod-xyz
```

---

## 🔹 Section 6: Monitoring & Logging

### Q14. 🟡 How do you monitor a Python backend?

**Answer:**
```python
# 1. Application Metrics — Prometheus + Grafana
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests',
                        ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds',
                            'Request latency')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.observe(duration)
    return response

# 2. Logging — ELK Stack (Elasticsearch + Logstash + Kibana)
import structlog
logger = structlog.get_logger()
logger.info("user_login", user_id=123, ip="1.2.3.4")

# 3. Error Tracking — Sentry
import sentry_sdk
sentry_sdk.init(dsn="https://your-sentry-dsn")

# 4. APM — New Relic, Datadog
```

**Monitoring stack:**
```
App → Prometheus (metrics) → Grafana (dashboards)
App → ELK/Loki (logs)     → Kibana/Grafana (search)
App → Sentry (errors)     → Alerts (Slack/PagerDuty)
```

---

### Q15. 🟡 What are health checks? How to implement them?

**Answer:**
```python
# FastAPI health check
@app.get("/health")
async def health_check():
    checks = {}
    
    # DB check
    try:
        await db.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception:
        checks["database"] = "unhealthy"
    
    # Redis check
    try:
        await redis.ping()
        checks["redis"] = "healthy"
    except Exception:
        checks["redis"] = "unhealthy"
    
    is_healthy = all(v == "healthy" for v in checks.values())
    return JSONResponse(
        status_code=200 if is_healthy else 503,
        content={"status": "healthy" if is_healthy else "unhealthy",
                 "checks": checks}
    )

# Kubernetes uses these for:
# livenessProbe  — Is app alive? (restart if not)
# readinessProbe — Is app ready? (remove from LB if not)
```

---

## 🔹 Section 7: Environment & Configuration

### Q16. 🟡 How do you manage environment variables?

**Answer:**
```python
# 1. .env file + python-dotenv
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
SECRET_KEY=super-secret-key
DEBUG=false

# settings.py
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# 2. Pydantic Settings (recommended for FastAPI)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

settings = Settings()

# 3. Docker → pass via docker-compose.yml or -e flag
# 4. K8s → ConfigMap and Secrets
```

---

### Q17. 🟢 What is `.env` vs `.env.example`?

**Answer:**
```bash
# .env — NEVER commit (has real secrets)
# Add to .gitignore!

# .env.example — Commit this (template for team)
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
SECRET_KEY=change-me
REDIS_URL=redis://localhost:6379/0
```

---

## 🔹 Section 8: Security & Best Practices

### Q18. 🟡 What security headers should your API have?

**Answer:**
```python
# FastAPI middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

---

### Q19. 🟡 How to handle secrets in production?

**Answer:**
```
Never in code or git!

Options:
1. Environment variables (basic)
2. AWS Secrets Manager / Parameter Store
3. HashiCorp Vault
4. K8s Secrets
5. Docker secrets

# AWS Secrets Manager
import boto3
client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='myapp/db-password')
password = json.loads(secret['SecretString'])['password']
```

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | Docker Image vs Container? | Blueprint vs Running instance |
| 2 | Docker Compose purpose? | Multi-container orchestration |
| 3 | CI vs CD? | Auto build/test vs Auto deploy |
| 4 | Nginx role? | Reverse proxy, static files, SSL |
| 5 | Gunicorn role? | WSGI server running Python app |
| 6 | K8s Pod? | Smallest deployable unit |
| 7 | Health check? | Endpoint to verify service status |
| 8 | IaC? | Manage infra via code (Terraform) |
| 9 | .env in git? | NEVER — use .env.example |
| 10 | Secrets storage? | Vault, AWS Secrets Manager, K8s Secrets |

---

*Next: [12_Coding_Round.md](12_Coding_Round.md)*
