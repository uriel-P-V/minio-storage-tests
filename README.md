# minio-storage-tests

![CI](https://github.com/uriel-P-V/minio-storage-tests/actions/workflows/tests.yml/badge.svg)

A storage test suite for MinIO object storage —
demonstrates real storage operations testing with Pytest,
including bucket lifecycle, object CRUD, performance benchmarks,
parametrized multi-size uploads, and a fully containerized CI/CD pipeline
with Docker and Allure Reports.

---

## Project Structure

```
minio-storage-tests/
├── .github/
│   └── workflows/
│       └── tests.yml          ← GitHub Actions CI with Docker + MinIO + Allure
├── tests/
│   ├── conftest.py            ← Session-scoped MinIO client fixture and test bucket fixture
│   ├── test_buckets.py        ← Bucket CRUD and error handling
│   ├── test_objects.py        ← Object upload, download, list, delete + parametrized sizes
│   └── test_performance.py    ← Latency benchmarks with pytest-benchmark
├── pytest.ini                 ← Marker definitions (smoke, regression)
└── requirements.txt
```

---

## Features

- **Real storage testing** — tests run against a live MinIO instance
- **Smoke & regression markers** — organized test execution with `pytest -m smoke` or `pytest -m regression`
- **Parametrized size testing** — upload tested with 1KB, 10KB and 100KB files automatically
- **Session-scoped fixture** — single MinIO connection shared across all tests for efficiency
- **Fixture with yield** — test bucket created before and cleaned up after each test
- **Error handling** — S3Error on duplicate buckets and missing objects
- **Performance benchmarks** — latency for upload, download and bucket creation
- **Allure Reports** — visual test report published to GitHub Pages after every CI run
- **Dockerized CI** — MinIO started via `docker run` in GitHub Actions pipeline

---

## Storage Operations Tested

| Operation | File | Description |
|-----------|------|-------------|
| Create bucket | test_buckets.py | Make and verify bucket exists |
| List buckets | test_buckets.py | Created bucket appears in list |
| Delete bucket | test_buckets.py | Bucket removed successfully |
| Duplicate bucket | test_buckets.py | S3Error raised on duplicate |
| Upload object | test_objects.py | PUT object to bucket |
| Download object | test_objects.py | GET and verify content matches |
| Object size | test_objects.py | Size matches uploaded data |
| Delete object | test_objects.py | Object removed from bucket |
| List objects | test_objects.py | Multiple objects appear in list |
| Missing object | test_objects.py | S3Error on GET nonexistent |
| Upload various sizes | test_objects.py | 1KB, 10KB, 100KB parametrized upload |
| Upload latency | test_performance.py | Mean < 200ms |
| Download latency | test_performance.py | Mean < 200ms |
| Bucket creation latency | test_performance.py | Mean < 500ms |

---

## Setup

### Prerequisites
- Docker Desktop installed and running
- Python 3.11+

### Run MinIO locally

```bash
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  quay.io/minio/minio server /data --console-address ":9001"
```

MinIO UI available at: `http://localhost:9001`

### Install dependencies and run tests

```bash
git clone https://github.com/uriel-P-V/minio-storage-tests.git
cd minio-storage-tests
pip install -r requirements.txt
pytest tests/ -v
```

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Smoke tests only (fast sanity checks)
pytest -m smoke -v

# Regression tests only (full suite)
pytest -m regression -v

# Buckets only
pytest tests/test_buckets.py -v

# Objects only
pytest tests/test_objects.py -v

# Performance benchmarks
pytest tests/test_performance.py -v

# With coverage
pytest tests/ --cov=tests --cov-report=term-missing

# Generate Allure results locally
pytest tests/ --alluredir=allure-results
```

---

## CI/CD Pipeline

GitHub Actions starts a MinIO container, runs all tests, and publishes an Allure Report to GitHub Pages:

```yaml
- name: Start MinIO
  run: |
    docker run -d --name minio \
      -p 9000:9000 \
      -e MINIO_ROOT_USER=minioadmin \
      -e MINIO_ROOT_PASSWORD=minioadmin \
      quay.io/minio/minio server /data

- name: Wait for MinIO to be ready
  run: |
    for i in {1..10}; do
      curl -f http://localhost:9000/minio/health/live && break
      sleep 3
    done
```

Allure Report published at: `https://uriel-p-v.github.io/minio-storage-tests`

---

## Tech Stack

- **Python 3.11+**
- **Pytest** — test framework with fixtures, markers and parametrize
- **MinIO Python SDK** — S3-compatible object storage client
- **pytest-benchmark** — performance and latency testing
- **pytest-cov** — coverage reporting
- **allure-pytest** — visual test reporting
- **Docker** — containerized MinIO for local and CI environments
- **GitHub Actions** — CI/CD pipeline with Allure deployment

---

## Author

**Uriel Alejandro Pérez Valdovinos**  
[github.com/uriel-P-V](https://github.com/uriel-P-V) · [linkedin.com/in/uriel-pv](https://linkedin.com/in/uriel-pv)