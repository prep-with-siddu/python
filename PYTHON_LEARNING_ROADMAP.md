# Python E2E Learning Roadmap — Basic to Advanced

> **One Course Recommendation + Supplementary Resources**
> Covers every topic from Core Python to Professional-Grade Engineering

---

## THE #1 RECOMMENDED COURSE

### **"100 Days of Code: The Complete Python Pro Bootcamp" — by Dr. Angela Yu (Udemy)**

- **Link:** [https://www.udemy.com/course/100-days-of-code/](https://www.udemy.com/course/100-days-of-code/)
- **Duration:** ~60+ hours of video content
- **Level:** Absolute Beginner → Professional
- **Projects:** 100 real-world projects (one per day)
- **Why this one?** It covers nearly every topic you listed — Core Python, OOP, File Handling, APIs, Databases, Testing, Debugging — all through hands-on projects. It's the most comprehensive single course available.

---

## HOW TO FOLLOW THIS COURSE — STEP-BY-STEP PATH

```
START HERE
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 1: FOUNDATIONS (Weeks 1–3)                       │
│  Course Days: 1–25                                      │
│                                                         │
│  ✦ Set up your environment first:                       │
│    → Install Python 3.12+ from python.org               │
│    → Install VS Code + Python extension                 │
│    → Create a virtual environment (venv)                │
│    → Learn to run .py files from terminal               │
│                                                         │
│  ✦ Follow course Days 1–25 sequentially                 │
│  ✦ Topics covered: Variables, Data Types, Strings,      │
│    Lists, Dictionaries, Loops, Functions, Error         │
│    Handling, Comprehensions, File I/O                   │
│                                                         │
│  ✦ After each day's lesson:                             │
│    → Code along (don't just watch)                      │
│    → Redo the project WITHOUT looking at solution       │
│    → Push your code to a GitHub repo daily              │
│                                                         │
│  ✦ Supplement with: Python Official Tutorial + Real     │
│    Python articles (linked in Section 1 below)          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 2: OOP & INTERMEDIATE (Weeks 4–5)                │
│  Course Days: 26–45                                     │
│                                                         │
│  ✦ Follow course Days 26–45                             │
│  ✦ Topics: Classes, Objects, Inheritance, Composition,  │
│    Encapsulation, Polymorphism, Dunder Methods          │
│                                                         │
│  ✦ Key practice:                                        │
│    → Build 2–3 mini projects using only OOP             │
│      (e.g., Library System, Bank Account, Quiz Game)    │
│    → Watch Corey Schafer's OOP playlist alongside       │
│                                                         │
│  ✦ Supplement with: Corey Schafer OOP YouTube playlist  │
│    + Real Python OOP articles (Section 2 below)         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 3: ADVANCED PYTHON (Weeks 6–7)                   │
│  Course Days: 46–60                                     │
│                                                         │
│  ✦ Follow course Days 46–60                             │
│  ✦ Topics: Decorators, Generators, Iterators, Context   │
│    Managers, Closures                                   │
│                                                         │
│  ✦ IMPORTANT — The course covers these lightly. You     │
│    MUST supplement with:                                │
│    → Real Python Decorators deep-dive                   │
│    → Real Python Generators article                     │
│    → Real Python Async IO walkthrough                   │
│    → Practice threading & multiprocessing separately    │
│      (Corey Schafer YouTube)                            │
│                                                         │
│  ✦ Self-study additions (not fully in course):          │
│    → async/await — follow Real Python Async IO guide    │
│    → Multithreading vs Multiprocessing — Corey Schafer  │
│    → Closures — Real Python closures article            │
│                                                         │
│  ✦ Supplement with: Section 3 resources below           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 4: FILE HANDLING & DATA (Week 8)                 │
│  Course Days: 61–70                                     │
│                                                         │
│  ✦ Follow course Days 61–70                             │
│  ✦ Topics: CSV, JSON, reading/writing files, pandas     │
│    basics, data parsing                                 │
│                                                         │
│  ✦ Practice project:                                    │
│    → Build a CSV/JSON data pipeline that reads,         │
│      transforms, and writes data                        │
│    → Parse a real API response (JSON) and save to CSV   │
│                                                         │
│  ✦ Supplement with: Section 4 resources below           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 5: APIs & NETWORKING (Weeks 9–10) ⭐ CRITICAL    │
│  Course Days: 71–82                                     │
│                                                         │
│  ✦ Follow course Days 71–82                             │
│  ✦ Topics: requests library, REST APIs, authentication, │
│    building APIs with Flask                             │
│                                                         │
│  ✦ MUST-DO extra work:                                  │
│    → Complete FastAPI official tutorial (separate)      │
│    → Build a full CRUD REST API from scratch            │
│    → Learn OAuth2 / JWT authentication                  │
│    → Practice with 3+ public APIs (weather, GitHub,     │
│      news, etc.)                                        │
│    → Use Postman to test your endpoints                 │
│                                                         │
│  ✦ Supplement with: Section 5 resources below           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 6: DATABASES (Week 10)                           │
│  Course Days: 83–88                                     │
│                                                         │
│  ✦ Follow course Days 83–88                             │
│  ✦ Topics: SQLite, SQLAlchemy basics                    │
│                                                         │
│  ✦ MUST-DO extra work:                                  │
│    → Learn raw SQL (SELECT, JOIN, INSERT, UPDATE)       │
│    → SQLAlchemy ORM tutorial (official docs)            │
│    → Connect your Phase 5 API to a real database        │
│    → Try PostgreSQL or MongoDB (one NoSQL experience)   │
│                                                         │
│  ✦ Supplement with: Section 6 resources below           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 7: TESTING, DEBUGGING, LOGGING (Week 11)         │
│  Course Days: 89–95                                     │
│                                                         │
│  ✦ The course covers testing lightly. You MUST          │
│    self-study:                                          │
│    → pytest full tutorial (Real Python)                 │
│    → unittest basics (Python docs)                      │
│    → Mocking with unittest.mock                         │
│    → Write tests for your Phase 5 & 6 projects          │
│                                                         │
│  ✦ Debugging & Logging (self-study):                    │
│    → Learn pdb + VS Code debugger                       │
│    → Set up logging module in a real project            │
│    → Learn cProfile for performance                     │
│                                                         │
│  ✦ Supplement with: Sections 7 & 8 resources below      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 8: PACKAGE MANAGEMENT & PRO WORKFLOW (Week 12)   │
│  Course Days: 96–100                                    │
│                                                         │
│  ✦ Learn and practice:                                  │
│    → venv / virtualenv setup                            │
│    → pip, requirements.txt, pip freeze                  │
│    → poetry or pipenv (modern tooling)                  │
│    → pyproject.toml structure                           │
│    → Docker basics for Python apps                      │
│    → Type hints + mypy                                  │
│    → Linting with ruff or flake8                        │
│                                                         │
│  ✦ Supplement with: Section 9 resources below           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 9: CAPSTONE PROJECT (Weeks 13–14)                │
│                                                         │
│  Build ONE full-stack project combining everything:     │
│                                                         │
│  ✦ Suggested Project: "Personal Finance API"            │
│    → FastAPI backend with REST endpoints                │
│    → PostgreSQL database with SQLAlchemy ORM            │
│    → JWT authentication                                 │
│    → CSV/JSON import-export                             │
│    → Full pytest test suite with 80%+ coverage          │
│    → Logging & error handling                           │
│    → Dockerized deployment                              │
│    → Clean package structure with pyproject.toml        │
│    → Type hints throughout                              │
│    → Push to GitHub with CI/CD (GitHub Actions)         │
│                                                         │
│  This single project proves you know Python E2E.        │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
                 ✅ DONE!
      You are now a professional Python developer.
      Next: Pick a specialization —
        → Backend (Django/FastAPI)
        → Data Science (Pandas/NumPy/ML)
        → DevOps (Automation/Scripting)
        → Systems Programming (Async/Networking)
```

### DAILY ROUTINE (Recommended)

| Time Block | Activity | Duration |
|---|---|---|
| Morning | Watch course lecture + code along | 1–1.5 hrs |
| Afternoon | Redo project solo (no peeking) | 1 hr |
| Evening | Read supplementary article (Real Python / Docs) | 30 min |
| Evening | Practice on LeetCode/HackerRank (2–3 problems) | 30 min |
| Anytime | Push code to GitHub | 5 min |

### KEY RULES TO FOLLOW

1. **Never just watch** — always code along in your own editor
2. **Build the project again from scratch** after each lesson without looking at the solution
3. **Push to GitHub daily** — this builds your portfolio and streak
4. **Read the error messages** — don't just Google, try to understand the traceback first
5. **Supplement the course** — Angela Yu's course doesn't cover async, threading, or advanced testing deeply; use the linked resources for those
6. **One topic at a time** — don't jump ahead; master each phase before moving on
7. **Build side projects** — after Phase 5, start building your own ideas
8. **Write tests** — even if the course doesn't ask for them, write tests for every project from Phase 7 onward

---

## TOPIC-BY-TOPIC BREAKDOWN WITH SUPPLEMENTARY RESOURCES

### 1. Core Python

| Topic | What to Learn |
|---|---|
| Data Types & Structures | `int`, `float`, `str`, `bool`, `list`, `tuple`, `set`, `dict`, `frozenset`, `bytes` |
| Comprehensions | List, Dict, Set, Nested comprehensions, Generator expressions |
| Functions | `*args`, `**kwargs`, lambda, `map()`, `filter()`, `reduce()`, first-class functions |
| Error Handling | `try/except/else/finally`, custom exceptions, exception chaining |
| Modules & Packages | `import`, `__init__.py`, relative imports, `sys.path`, creating packages |

**Video Tutorials (Validated):**
- Mosh — Python Full Course for Beginners (6 hrs): [https://www.youtube.com/watch?v=_uQrJ0TkZlc](https://www.youtube.com/watch?v=_uQrJ0TkZlc)
- freeCodeCamp — Learn Python Full Course (4.5 hrs): [https://www.youtube.com/watch?v=rfscVS0vtbw](https://www.youtube.com/watch?v=rfscVS0vtbw)
- Corey Schafer — Comprehensions: [https://www.youtube.com/watch?v=3dt4OGnU5sM](https://www.youtube.com/watch?v=3dt4OGnU5sM)
- Corey Schafer — Try/Except Error Handling: [https://www.youtube.com/watch?v=NIWwJbo-9_8](https://www.youtube.com/watch?v=NIWwJbo-9_8)
- Corey Schafer — Import Modules & Packages: [https://www.youtube.com/watch?v=CqvZ3vGoGs0](https://www.youtube.com/watch?v=CqvZ3vGoGs0)
- Corey Schafer — Full Python Playlist: [https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU)

**Supplementary Resources:**
- Official Python Tutorial: [https://docs.python.org/3/tutorial/](https://docs.python.org/3/tutorial/)
- Python Docs — Data Structures: [https://docs.python.org/3/tutorial/datastructures.html](https://docs.python.org/3/tutorial/datastructures.html)
- Real Python — Comprehensions: [https://realpython.com/list-comprehension-python/](https://realpython.com/list-comprehension-python/)
- Real Python — Functions: [https://realpython.com/defining-your-own-python-function/](https://realpython.com/defining-your-own-python-function/)
- Real Python — Exceptions: [https://realpython.com/python-exceptions/](https://realpython.com/python-exceptions/)

---

### 2. Object-Oriented Programming (OOP)

| Topic | What to Learn |
|---|---|
| Classes & Objects | `__init__`, instance vs class attributes, `self`, class methods, static methods |
| Inheritance & Composition | Single/multiple/multilevel inheritance, MRO, mixins, composition over inheritance |
| Encapsulation | Name mangling (`__private`), `_protected`, property decorators, getters/setters |
| Polymorphism | Method overriding, duck typing, abstract base classes (`ABC`) |
| Dunder Methods | `__str__`, `__repr__`, `__len__`, `__getitem__`, `__eq__`, `__hash__`, `__call__`, `__enter__/__exit__` |

**Video Tutorials (Validated):**
- Corey Schafer — OOP Full Playlist (6 videos): [https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc](https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc)
- Corey Schafer — OOP 1: Classes and Instances: [https://www.youtube.com/watch?v=ZDa-Z5JzLYM](https://www.youtube.com/watch?v=ZDa-Z5JzLYM)
- Corey Schafer — OOP 5: Special (Magic/Dunder) Methods: [https://www.youtube.com/watch?v=3ohzBxoFHAY](https://www.youtube.com/watch?v=3ohzBxoFHAY)
- Corey Schafer — OOP 6: Property Decorators (Getters/Setters): [https://www.youtube.com/watch?v=jCzT9XFZ5bw](https://www.youtube.com/watch?v=jCzT9XFZ5bw)
- Tech With Tim — Intermediate Python Programming Course (6 hrs): [https://www.youtube.com/watch?v=HGOBQPFzWKo](https://www.youtube.com/watch?v=HGOBQPFzWKo)

**Supplementary Resources:**
- Real Python — OOP: [https://realpython.com/python3-object-oriented-programming/](https://realpython.com/python3-object-oriented-programming/)
- Python Docs — Data Model (Dunder Methods): [https://docs.python.org/3/reference/datamodel.html](https://docs.python.org/3/reference/datamodel.html)
- Real Python — Inheritance & Composition: [https://realpython.com/inheritance-composition-python/](https://realpython.com/inheritance-composition-python/)

---

### 3. Advanced Python

| Topic | What to Learn |
|---|---|
| Decorators | Function decorators, class decorators, `functools.wraps`, decorator factories, stacking |
| Generators & Iterators | `yield`, `yield from`, iterator protocol (`__iter__`, `__next__`), `itertools` |
| Context Managers | `with` statement, `__enter__/__exit__`, `contextlib.contextmanager` |
| Closures | Nested functions, `nonlocal`, closure use cases |
| Multithreading vs Multiprocessing | `threading`, `multiprocessing`, GIL, `concurrent.futures`, thread pools, process pools |
| Async Programming | `async/await`, `asyncio`, event loops, `aiohttp`, async generators |

**Video Tutorials (Validated):**
- Corey Schafer — Decorators: [https://www.youtube.com/watch?v=FsAPt_9Bf3U](https://www.youtube.com/watch?v=FsAPt_9Bf3U)
- Corey Schafer — Generators: [https://www.youtube.com/watch?v=bD05uGo_sVI](https://www.youtube.com/watch?v=bD05uGo_sVI)
- Corey Schafer — Context Managers: [https://www.youtube.com/watch?v=-aKFBoZpiqA](https://www.youtube.com/watch?v=-aKFBoZpiqA)
- Corey Schafer — Closures: [https://www.youtube.com/watch?v=swU3c34d2NQ](https://www.youtube.com/watch?v=swU3c34d2NQ)
- Corey Schafer — Threading: [https://www.youtube.com/watch?v=IEEhzQoKtQU](https://www.youtube.com/watch?v=IEEhzQoKtQU)
- Corey Schafer — Multiprocessing: [https://www.youtube.com/watch?v=fKl2JW_qrso](https://www.youtube.com/watch?v=fKl2JW_qrso)
- Corey Schafer — Itertools Module: [https://www.youtube.com/watch?v=Qu3dThVy6KQ](https://www.youtube.com/watch?v=Qu3dThVy6KQ)
- Async Programming — AsyncIO & Async/Await: [https://www.youtube.com/watch?v=t5Bo1Je9EmE](https://www.youtube.com/watch?v=t5Bo1Je9EmE)
- Asyncio for Beginners: [https://www.youtube.com/watch?v=2IW-ZEui4h4](https://www.youtube.com/watch?v=2IW-ZEui4h4)

**Supplementary Resources:**
- Real Python — Decorators: [https://realpython.com/primer-on-python-decorators/](https://realpython.com/primer-on-python-decorators/)
- Real Python — Generators: [https://realpython.com/introduction-to-python-generators/](https://realpython.com/introduction-to-python-generators/)
- Real Python — Context Managers: [https://realpython.com/python-with-statement/](https://realpython.com/python-with-statement/)
- Real Python — Concurrency: [https://realpython.com/python-concurrency/](https://realpython.com/python-concurrency/)
- Real Python — Async IO: [https://realpython.com/async-io-python/](https://realpython.com/async-io-python/)
- Python Docs — asyncio: [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)

---

### 4. File Handling & Data Processing

| Topic | What to Learn |
|---|---|
| File I/O | `open()`, read/write modes, `with` statement, binary files |
| CSV | `csv` module, `csv.DictReader`, `csv.DictWriter` |
| JSON | `json.load()`, `json.dump()`, `json.loads()`, `json.dumps()`, nested JSON |
| Large Datasets | Chunked reading, `pandas` for large CSVs, memory-efficient processing |
| Data Parsing | `re` (regex), `xml.etree`, `BeautifulSoup`, `lxml` |

**Video Tutorials (Validated):**
- Corey Schafer — File Objects (Reading & Writing Files): [https://www.youtube.com/watch?v=Uh2ebFW8OYM](https://www.youtube.com/watch?v=Uh2ebFW8OYM)
- Corey Schafer — CSV Module (Read, Parse, Write): [https://www.youtube.com/watch?v=q5uM4VKywbA](https://www.youtube.com/watch?v=q5uM4VKywbA)
- Corey Schafer — Working with JSON Data: [https://www.youtube.com/watch?v=9N6a-VLBa2I](https://www.youtube.com/watch?v=9N6a-VLBa2I)

**Supplementary Resources:**
- Real Python — File I/O: [https://realpython.com/read-write-files-python/](https://realpython.com/read-write-files-python/)
- Real Python — Working with JSON: [https://realpython.com/python-json/](https://realpython.com/python-json/)
- Real Python — CSV: [https://realpython.com/python-csv/](https://realpython.com/python-csv/)
- Pandas Official Docs: [https://pandas.pydata.org/docs/getting_started/](https://pandas.pydata.org/docs/getting_started/)
- Real Python — Regex: [https://realpython.com/regex-python/](https://realpython.com/regex-python/)

---

### 5. APIs & Networking (Very Important)

| Topic | What to Learn |
|---|---|
| REST APIs | HTTP methods (GET, POST, PUT, DELETE), status codes, headers |
| `requests` Library | Making API calls, authentication, headers, query params, sessions |
| Building APIs | Flask / FastAPI — creating endpoints, request/response models |
| Authentication | API keys, OAuth 2.0, JWT tokens, Bearer tokens |
| WebSockets | Real-time communication, `websockets` library |
| Serialization | JSON serialization/deserialization, Pydantic models |

**Video Tutorials (Validated):**
- freeCodeCamp — Python API Development Full Course (19 hrs): [https://www.youtube.com/watch?v=0sOvCWFmrtA](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- freeCodeCamp — FastAPI Course for Beginners: [https://www.youtube.com/watch?v=tLKKmouUams](https://www.youtube.com/watch?v=tLKKmouUams)
- freeCodeCamp — Learn Flask for Python Full Tutorial: [https://www.youtube.com/watch?v=Z1RJmh_OqeA](https://www.youtube.com/watch?v=Z1RJmh_OqeA)

**Supplementary Resources:**
- Real Python — APIs: [https://realpython.com/api-integration-in-python/](https://realpython.com/api-integration-in-python/)
- Real Python — `requests`: [https://realpython.com/python-requests/](https://realpython.com/python-requests/)
- FastAPI Official Docs: [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/)
- Flask Official Tutorial: [https://flask.palletsprojects.com/en/stable/tutorial/](https://flask.palletsprojects.com/en/stable/tutorial/)
- Real Python — Flask REST API: [https://realpython.com/flask-connexion-rest-api/](https://realpython.com/flask-connexion-rest-api/)
- Postman Learning Center: [https://learning.postman.com/docs/getting-started/introduction/](https://learning.postman.com/docs/getting-started/introduction/)

---

### 6. Database Integration

| Topic | What to Learn |
|---|---|
| SQL Basics | SELECT, INSERT, UPDATE, DELETE, JOINs, indexes |
| SQLite | `sqlite3` module, CRUD operations, parameterized queries |
| PostgreSQL / MySQL | `psycopg2`, `mysql-connector-python`, connection pooling |
| ORM | SQLAlchemy — models, sessions, queries, relationships, migrations (Alembic) |
| NoSQL | MongoDB with `pymongo`, Redis with `redis-py` |
| Connection Management | Context managers for DB connections, connection pooling |

**Video Tutorials (Validated):**
- freeCodeCamp — SQLite Databases With Python Full Course: [https://www.youtube.com/watch?v=byHcYRpMgI4](https://www.youtube.com/watch?v=byHcYRpMgI4)
- Corey Schafer — Flask-SQLAlchemy (Database ORM): [https://www.youtube.com/watch?v=cYWiDiIUxQc](https://www.youtube.com/watch?v=cYWiDiIUxQc)

**Supplementary Resources:**
- Real Python — SQLite: [https://realpython.com/python-sqlite-sqlalchemy/](https://realpython.com/python-sqlite-sqlalchemy/)
- SQLAlchemy Official Tutorial: [https://docs.sqlalchemy.org/en/20/tutorial/](https://docs.sqlalchemy.org/en/20/tutorial/)
- Real Python — MongoDB: [https://realpython.com/introduction-to-mongodb-and-python/](https://realpython.com/introduction-to-mongodb-and-python/)
- PostgreSQL + Python: [https://realpython.com/python-sql-libraries/](https://realpython.com/python-sql-libraries/)

---

### 7. Testing

| Topic | What to Learn |
|---|---|
| `unittest` | Test cases, assertions, setUp/tearDown, test suites, mocking |
| `pytest` | Fixtures, parametrize, markers, conftest.py, plugins |
| Mocking | `unittest.mock`, `patch`, `MagicMock`, mocking APIs & DBs |
| Coverage | `coverage.py`, `pytest-cov`, measuring test coverage |
| TDD | Test-Driven Development workflow — Red, Green, Refactor |
| Integration Testing | Testing API endpoints, database integration tests |

**Video Tutorials (Validated):**
- Corey Schafer — Unit Testing with unittest Module: [https://www.youtube.com/watch?v=6tNS--WetLI](https://www.youtube.com/watch?v=6tNS--WetLI)
- Pytest Tutorial — How To Write Unit Tests in Python: [https://www.youtube.com/watch?v=YbpKMIUjvK8](https://www.youtube.com/watch?v=YbpKMIUjvK8)

**Supplementary Resources:**
- Real Python — pytest: [https://realpython.com/pytest-python-testing/](https://realpython.com/pytest-python-testing/)
- Real Python — Mocking: [https://realpython.com/python-mock-library/](https://realpython.com/python-mock-library/)
- pytest Official Docs: [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/)
- Real Python — TDD: [https://realpython.com/python-testing/](https://realpython.com/python-testing/)

---

### 8. Debugging & Logging

| Topic | What to Learn |
|---|---|
| Debugging | `pdb`, `breakpoint()`, VS Code debugger, conditional breakpoints |
| Logging | `logging` module, log levels, handlers, formatters, rotating logs |
| Profiling | `cProfile`, `line_profiler`, `memory_profiler`, identifying bottlenecks |
| Tracing | `traceback` module, stack traces, `sys.exc_info()` |

**Video Tutorials (Validated):**
- Corey Schafer — Logging Basics (Levels, Files, Formatting): [https://www.youtube.com/watch?v=-ARI4Cz-awo](https://www.youtube.com/watch?v=-ARI4Cz-awo)
- Nina Zakharenko — Goodbye Print, Hello Debugger! (PyCon Talk): [https://www.youtube.com/watch?v=5AYIe-3cD-s](https://www.youtube.com/watch?v=5AYIe-3cD-s)

**Supplementary Resources:**
- Real Python — Logging: [https://realpython.com/python-logging/](https://realpython.com/python-logging/)
- Real Python — pdb Debugging: [https://realpython.com/python-debugging-pdb/](https://realpython.com/python-debugging-pdb/)
- Python Docs — Logging HOWTO: [https://docs.python.org/3/howto/logging.html](https://docs.python.org/3/howto/logging.html)
- Real Python — Profiling: [https://realpython.com/python-profiling/](https://realpython.com/python-profiling/)

---

### 9. Package Management & Environment

| Topic | What to Learn |
|---|---|
| Virtual Environments | `venv`, `virtualenv`, creating/activating/deactivating |
| Package Management | `pip`, `pip freeze`, `requirements.txt`, `pip install -e .` |
| Modern Tools | `poetry`, `pipenv`, `uv`, `pyproject.toml` |
| Dependency Resolution | Lock files, version pinning, dependency conflicts |
| Publishing Packages | `setup.py`, `pyproject.toml`, uploading to PyPI, `twine` |
| Docker | Dockerizing Python apps, multi-stage builds |

**Video Tutorials (Validated):**
- Corey Schafer — VENV: How to Use Virtual Environments (Mac & Linux): [https://www.youtube.com/watch?v=Kg1Yvry_Ydk](https://www.youtube.com/watch?v=Kg1Yvry_Ydk)
- Docker Tutorial — How To Containerize Python Applications: [https://www.youtube.com/watch?v=bi0cKgmRuiA](https://www.youtube.com/watch?v=bi0cKgmRuiA)

**Supplementary Resources:**
- Real Python — Virtual Environments: [https://realpython.com/python-virtual-environments-a-primer/](https://realpython.com/python-virtual-environments-a-primer/)
- Real Python — pip: [https://realpython.com/what-is-pip/](https://realpython.com/what-is-pip/)
- Poetry Docs: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
- Real Python — Publishing Packages: [https://realpython.com/pypi-publish-python-package/](https://realpython.com/pypi-publish-python-package/)
- Docker + Python: [https://docs.docker.com/language/python/](https://docs.docker.com/language/python/)

---

## BONUS TOPICS YOU MISSED (Professional-Level)

### 10. Design Patterns in Python
- Singleton, Factory, Observer, Strategy, Decorator pattern
- Video — Design Patterns in Python (PyCon Talk): [https://www.youtube.com/watch?v=o1FZ_Bd4DSM](https://www.youtube.com/watch?v=o1FZ_Bd4DSM)
- Real Python — Design Patterns: [https://realpython.com/factory-method-python/](https://realpython.com/factory-method-python/)

### 11. Type Hints & Static Analysis
- Type annotations, `typing` module, `mypy`, `Pydantic`
- Real Python — Type Checking: [https://realpython.com/python-type-checking/](https://realpython.com/python-type-checking/)

### 12. Security Best Practices
- Input validation, SQL injection prevention, secrets management, `hashlib`, `secrets` module
- OWASP Python Security: [https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)

### 13. Performance Optimization
- `Cython`, `NumPy` vectorization, memoization (`functools.lru_cache`), `__slots__`
- Real Python — Performance Tips: [https://realpython.com/python-performance/](https://realpython.com/python-performance/)

### 14. CI/CD & DevOps with Python
- GitHub Actions, pre-commit hooks, linting (`ruff`, `flake8`, `black`)
- Real Python — CI/CD: [https://realpython.com/python-continuous-integration/](https://realpython.com/python-continuous-integration/)

### 15. Web Scraping
- `BeautifulSoup`, `Scrapy`, `Selenium`, `Playwright`
- Real Python — Web Scraping: [https://realpython.com/beautiful-soup-web-scraper-python/](https://realpython.com/beautiful-soup-web-scraper-python/)

### 16. Data Science & ML Foundations (Optional but High Value)
- `NumPy`, `Pandas`, `Matplotlib`, `scikit-learn` basics
- Kaggle Free Python Course: [https://www.kaggle.com/learn/python](https://www.kaggle.com/learn/python)
- Kaggle Pandas Course: [https://www.kaggle.com/learn/pandas](https://www.kaggle.com/learn/pandas)

---

## FREE ALTERNATIVES TO THE MAIN COURSE

| Resource | Link | Notes |
|---|---|---|
| CS50's Introduction to Python (Harvard) | [https://cs50.harvard.edu/python/](https://cs50.harvard.edu/python/) | Free, world-class, covers basics to intermediate |
| freeCodeCamp Python (YouTube — 12 hrs) | [https://www.youtube.com/watch?v=rfscVS0vtbw](https://www.youtube.com/watch?v=rfscVS0vtbw) | Great for beginners |
| Corey Schafer Python Playlist (YouTube) | [https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) | Best free advanced Python content |
| Tech With Tim — Python (YouTube) | [https://www.youtube.com/c/TechWithTim](https://www.youtube.com/c/TechWithTim) | Projects-focused learning |
| Python Official Docs | [https://docs.python.org/3/](https://docs.python.org/3/) | The ultimate reference |
| Automate the Boring Stuff (Free Book) | [https://automatetheboringstuff.com/](https://automatetheboringstuff.com/) | Practical Python automation |
| Real Python (Articles + Tutorials) | [https://realpython.com/](https://realpython.com/) | Best written tutorials for every topic |

---

## RECOMMENDED BOOKS (For Deep Understanding)

| Book | Author | Level |
|---|---|---|
| Python Crash Course | Eric Matthes | Beginner |
| Automate the Boring Stuff with Python | Al Sweigart | Beginner–Intermediate |
| Fluent Python (2nd Edition) | Luciano Ramalho | Intermediate–Advanced |
| Effective Python | Brett Slatkin | Intermediate–Advanced |
| Python Cookbook | David Beazley | Advanced |
| Architecture Patterns with Python | Harry Percival & Bob Gregory | Professional |

---

## SUGGESTED LEARNING ORDER (12-WEEK PLAN)

| Week | Topics | Focus |
|---|---|---|
| 1–2 | Core Python (Data types, functions, comprehensions) | Build strong foundations |
| 3–4 | OOP (Classes, inheritance, dunder methods) | Think in objects |
| 5–6 | Advanced Python (Decorators, generators, closures, context managers) | Write Pythonic code |
| 7 | File Handling & Data Processing (CSV, JSON, regex) | Real-world data work |
| 8–9 | APIs & Networking (requests, FastAPI/Flask, auth) | Backend engineering |
| 9–10 | Database Integration (SQLite, PostgreSQL, SQLAlchemy) | Data persistence |
| 10–11 | Testing & Debugging (pytest, logging, profiling) | Quality assurance |
| 11–12 | Package Management, CI/CD, Docker, Type Hints | Professional workflow |

---

## PRACTICE PLATFORMS

| Platform | Link |
|---|---|
| LeetCode (Python) | [https://leetcode.com/](https://leetcode.com/) |
| HackerRank (Python) | [https://www.hackerrank.com/domains/python](https://www.hackerrank.com/domains/python) |
| Codewars | [https://www.codewars.com/](https://www.codewars.com/) |
| Exercism (Python Track) | [https://exercism.org/tracks/python](https://exercism.org/tracks/python) |
| Project Euler | [https://projecteuler.net/](https://projecteuler.net/) |
| Real Python Quizzes | [https://realpython.com/quizzes/](https://realpython.com/quizzes/) |

---

> **TL;DR:** Start with **Angela Yu's 100 Days of Code** on Udemy as your single primary course.
> Supplement each topic with **Real Python** articles and **Corey Schafer's** YouTube tutorials.
> For deep mastery, read **Fluent Python** by Luciano Ramalho.

---

*Generated: March 2026 | File: PYTHON_LEARNING_ROADMAP.md*
