# 09 — Testing — Interview Questions

> **35+ questions covering pytest, unittest, mocking, TDD, integration testing, coverage**

---

## 🔹 Section 1: Testing Fundamentals

### Q1. 🟢 What are the types of testing?

**Answer:**

| Type | Scope | Speed | Example |
|------|-------|-------|---------|
| **Unit test** | Single function/class | Fast | Test `add(2, 3) == 5` |
| **Integration test** | Multiple components | Medium | Test API → DB → Response |
| **End-to-End (E2E)** | Full workflow | Slow | Test user signup flow |
| **Smoke test** | Basic functionality | Fast | Check server starts |
| **Regression test** | Previously fixed bugs | Varies | Ensure bug doesn't return |
| **Load/Performance** | Scalability | Slow | 1000 concurrent requests |

**Testing pyramid:**
```
    /  E2E  \        ← Few, slow, expensive
   / Integration \   ← Some
  /   Unit Tests  \  ← Many, fast, cheap
```

---

### Q2. 🟢 What is the difference between `unittest` and `pytest`?

**Answer:**

| Feature | unittest | pytest |
|---------|----------|--------|
| Style | Class-based (Java-like) | Function-based |
| Assertions | `self.assertEqual()` | Plain `assert` |
| Fixtures | `setUp`/`tearDown` | `@pytest.fixture` |
| Discovery | Manual | Auto-discovers `test_*.py` |
| Plugins | Limited | 800+ plugins |
| Output | Basic | Rich, colored |
| Parametrize | Hard | `@pytest.mark.parametrize` |

```python
# unittest
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
    
    def tearDown(self):
        pass

# pytest (simpler!)
import pytest

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

---

### Q3. 🟢 How to run pytest?

**Answer:**
```bash
# Run all tests
pytest

# Run specific file
pytest test_users.py

# Run specific test
pytest test_users.py::test_create_user

# Run with verbose output
pytest -v

# Run with print output
pytest -s

# Run failed tests only
pytest --lf

# Run with coverage
pytest --cov=src --cov-report=html

# Run tests matching keyword
pytest -k "login or signup"

# Run marked tests
pytest -m "slow"

# Stop on first failure
pytest -x
```

---

## 🔹 Section 2: Pytest Deep Dive

### Q4. 🟡 What are pytest fixtures?

**Answer:**
Fixtures provide reusable setup/teardown for tests.

```python
import pytest

@pytest.fixture
def user():
    """Create a test user."""
    return {"name": "Sid", "email": "sid@test.com"}

@pytest.fixture
def db_session():
    """Database session with cleanup."""
    session = create_session()
    yield session          # Test runs here
    session.rollback()     # Cleanup after test
    session.close()

# Use fixtures
def test_create_user(db_session, user):
    result = db_session.add(User(**user))
    assert result.name == "Sid"
```

**Fixture scopes:**
```python
@pytest.fixture(scope="function")   # Default — per test
@pytest.fixture(scope="class")      # Per test class
@pytest.fixture(scope="module")     # Per file
@pytest.fixture(scope="session")    # Once for entire run

# Example: expensive DB setup
@pytest.fixture(scope="session")
def database():
    db = create_database()
    run_migrations(db)
    yield db
    db.drop_all()
```

---

### Q5. 🟡 What is `conftest.py`?

**Answer:**
`conftest.py` = Shared fixtures available to all tests in the directory.

```
tests/
├── conftest.py          ← Fixtures for all tests
├── test_users.py
├── api/
│   ├── conftest.py      ← Fixtures for API tests only
│   └── test_endpoints.py
```

```python
# tests/conftest.py
import pytest
from app import create_app

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers():
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}
```

---

### Q6. 🟡 What is parametrize in pytest?

**Answer:**
Run same test with different inputs.

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (1, False),
])
def test_is_prime(input, expected):
    assert is_prime(input) == expected

# Multiple parameters
@pytest.mark.parametrize("a,b,result", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, result):
    assert add(a, b) == result
```

---

### Q7. 🟡 What are pytest markers?

**Answer:**
```python
import pytest

@pytest.mark.slow
def test_large_export():
    """Slow test — skip in CI fast runs."""
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Requires Unix")
def test_unix_only():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    pass

# pytest.ini or pyproject.toml
# [tool.pytest.ini_options]
# markers = [
#     "slow: marks tests as slow",
# ]
```

---

## 🔹 Section 3: Mocking

### Q8. 🟡 What is mocking? Why is it important?

**Answer:**
Mocking replaces real objects with fake ones to isolate units.

**Why mock?**
- Don't call real APIs in tests
- Don't send real emails
- Don't hit real databases
- Test edge cases (errors, timeouts)
- Speed up tests

```python
from unittest.mock import Mock, patch, MagicMock

# Simple mock
mock_db = Mock()
mock_db.get_user.return_value = {"id": 1, "name": "Sid"}
result = mock_db.get_user(1)
assert result["name"] == "Sid"
mock_db.get_user.assert_called_once_with(1)
```

---

### Q9. 🟡 Explain `patch`, `Mock`, and `MagicMock`.

**Answer:**
```python
from unittest.mock import patch, Mock, MagicMock

# Mock — basic mock object
mock = Mock()
mock.method.return_value = 42
assert mock.method() == 42

# MagicMock — Mock + magic methods (__len__, __getitem__, etc.)
magic = MagicMock()
magic.__len__.return_value = 5
assert len(magic) == 5

# patch — replace real object with mock
@patch('myapp.services.send_email')
def test_signup(mock_send_email):
    mock_send_email.return_value = True
    result = signup("sid@test.com")
    assert result == "success"
    mock_send_email.assert_called_once_with("sid@test.com")

# patch as context manager
def test_api_call():
    with patch('myapp.client.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}
        result = fetch_data()
        assert result == {"data": "test"}
```

---

### Q10. 🟡 How to mock external API calls?

**Answer:**
```python
import requests
from unittest.mock import patch

def get_weather(city):
    response = requests.get(f"https://api.weather.com/{city}")
    if response.status_code == 200:
        return response.json()["temp"]
    return None

# Test
@patch('myapp.weather.requests.get')
def test_get_weather(mock_get):
    # Mock successful response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temp": 25}
    
    assert get_weather("bangalore") == 25
    
    # Mock failure
    mock_get.return_value.status_code = 500
    assert get_weather("bangalore") is None

# Using responses library (cleaner)
import responses

@responses.activate
def test_get_weather():
    responses.add(
        responses.GET,
        "https://api.weather.com/bangalore",
        json={"temp": 25},
        status=200
    )
    assert get_weather("bangalore") == 25
```

---

### Q11. 🟡 How do you mock database operations?

**Answer:**
```python
# Method 1: Mock the DB session
@patch('myapp.db.session')
def test_create_user(mock_session):
    user = create_user("Sid", "sid@test.com")
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

# Method 2: Use test database (integration test)
@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_user_crud(test_db):
    user = User(name="Sid", email="sid@test.com")
    test_db.add(user)
    test_db.commit()
    assert test_db.query(User).count() == 1
```

---

## 🔹 Section 4: Testing Web Applications

### Q12. 🟡 How to test a FastAPI application?

**Answer:**
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    response = client.post("/api/users", json={
        "name": "Sid",
        "email": "sid@test.com"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Sid"

def test_user_not_found():
    response = client.get("/api/users/9999")
    assert response.status_code == 404

# Async test
import pytest

@pytest.mark.anyio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users")
    assert response.status_code == 200
```

---

### Q13. 🟡 How to test a Flask application?

**Answer:**
```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/api/users",
        json={"name": "Sid", "email": "sid@test.com"})
    assert response.status_code == 201
```

---

### Q14. 🟡 How to test Django views?

**Answer:**
```python
from django.test import TestCase, Client
from django.urls import reverse

class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="sid", password="test123"
        )
    
    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'sid',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_user_list(self):
        self.client.login(username='sid', password='test123')
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sid')
```

---

## 🔹 Section 5: TDD & Best Practices

### Q15. 🟡 What is TDD (Test-Driven Development)?

**Answer:**
```
TDD Cycle: Red → Green → Refactor

1. RED     — Write a failing test first
2. GREEN   — Write minimal code to pass
3. REFACTOR — Improve code, keep tests green
```

```python
# Step 1: RED — Write failing test
def test_fizzbuzz():
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(7) == "7"
# NameError: fizzbuzz is not defined

# Step 2: GREEN — Minimal implementation
def fizzbuzz(n):
    if n % 15 == 0: return "FizzBuzz"
    if n % 3 == 0: return "Fizz"
    if n % 5 == 0: return "Buzz"
    return str(n)
# All tests pass ✅

# Step 3: REFACTOR — Improve
def fizzbuzz(n):
    result = ""
    if n % 3 == 0: result += "Fizz"
    if n % 5 == 0: result += "Buzz"
    return result or str(n)
```

---

### Q16. 🟡 What is code coverage? How to measure it?

**Answer:**
```bash
# Install
pip install pytest-cov

# Run with coverage
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html

# Coverage config in pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

**Coverage types:**
- **Line coverage** — Which lines were executed
- **Branch coverage** — Which if/else branches were taken
- **Function coverage** — Which functions were called

**Tip:** 100% coverage ≠ bug-free. Focus on meaningful tests, not coverage %.

---

### Q17. 🟢 What are testing best practices?

**Answer:**
```python
# 1. AAA Pattern — Arrange, Act, Assert
def test_user_creation():
    # Arrange
    data = {"name": "Sid", "email": "sid@test.com"}
    
    # Act
    user = create_user(**data)
    
    # Assert
    assert user.name == "Sid"
    assert user.email == "sid@test.com"

# 2. One assertion per concept
# 3. Descriptive test names
def test_login_fails_with_wrong_password():  # ✅ Clear
def test_login():                             # ❌ Vague

# 4. Don't test implementation — test behavior
# 5. Use factories for test data
# 6. Keep tests independent (no shared state)
# 7. Fast tests (mock external dependencies)
# 8. Test edge cases (empty, null, boundary values)
```

---

## 🔹 Section 6: Advanced Testing

### Q18. 🔴 What is property-based testing?

**Answer:**
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)

@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    assert len(sorted(lst)) == len(lst)

@given(st.text(min_size=1))
def test_reverse_twice(s):
    assert s[::-1][::-1] == s
```

---

### Q19. 🟡 How to test async code?

**Answer:**
```python
import pytest
import asyncio

# pytest-asyncio
@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("https://api.example.com")
    assert result is not None

# Mocking async functions
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_service():
    mock_db = AsyncMock()
    mock_db.get_user.return_value = {"name": "Sid"}
    
    result = await mock_db.get_user(1)
    assert result["name"] == "Sid"
```

---

### Q20. 🟡 What is snapshot testing?

**Answer:**
```python
# pytest-snapshot or syrupy
def test_user_response(snapshot):
    response = client.get("/api/users/1")
    assert response.json() == snapshot
    
# First run: creates snapshot file
# Next runs: compares against saved snapshot
# Update snapshots: pytest --snapshot-update
```

**Use cases:** API response structures, serialized output, HTML rendering

---

## 🔹 Quick Revision — One-Liners

| # | Question | Answer |
|---|----------|--------|
| 1 | Testing pyramid? | Unit (most) → Integration → E2E (least) |
| 2 | pytest vs unittest? | Function-based + plain assert vs Class-based |
| 3 | Fixture scope? | function, class, module, session |
| 4 | conftest.py? | Shared fixtures auto-discovered by pytest |
| 5 | Mock purpose? | Isolate unit from external dependencies |
| 6 | patch target? | Where it's used, not where it's defined |
| 7 | TDD cycle? | Red → Green → Refactor |
| 8 | Coverage goal? | 80%+ meaningful, not 100% blind |
| 9 | AAA pattern? | Arrange → Act → Assert |
| 10 | Property testing? | Random input testing with Hypothesis |

---

*Next: [10_System_Design_Architecture.md](10_System_Design_Architecture.md)*
