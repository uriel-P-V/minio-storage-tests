# minio-storage-tests

![CI](https://github.com/uriel-P-V/minio-storage-tests/actions/workflows/tests.yml/badge.svg)

A storage test suite for MinIO object storage —
demonstrates real storage operations testing with Pytest,
including bucket lifecycle, object CRUD, performance benchmarks,
and a fully containerized CI/CD pipeline with Docker.

---

## Project Structure

```
minio-storage-tests/
├── .github/
│   └── workflows/
│       └── tests.yml          ← GitHub Actions CI with Docker + MinIO
├── tests/
│   ├── conftest.py            ← MinIO client fixture and test bucket fixture
│   ├── test_buckets.py        ← Bucket CRUD and error handling
│   ├── test_objects.py        ← Object upload, download, list, delete
│   └── test_performance.py    ← Latency benchmarks with pytest-benchmark
└── requirements.txt
```

---

## Features

- **Real storage testing** — tests run against a live MinIO instance
- **Fixture with yield** — test bucket created before and cleaned up after each test
- **Error handling** — S3Error on duplicate buckets and missing objects
- **Performance benchmarks** — latency for upload, download and bucket creation
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

# Buckets only
pytest tests/test_buckets.py -v

# Objects only
pytest tests/test_objects.py -v

# Performance benchmarks
pytest tests/test_performance.py -v

# With coverage
pytest tests/ --cov=tests --cov-report=term-missing
```

---

## CI/CD Pipeline

GitHub Actions starts a MinIO container before running tests:

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

---

## Tech Stack

- **Python 3.11+**
- **Pytest** — test framework with fixtures and markers
- **MinIO Python SDK** — S3-compatible object storage client
- **pytest-benchmark** — performance and latency testing
- **pytest-cov** — coverage reporting
- **Docker** — containerized MinIO for local and CI environments
- **GitHub Actions** — CI/CD pipeline

---

## Author

**Uriel Alejandro Pérez Valdovinos**  
[github.com/uriel-P-V](https://github.com/uriel-P-V) · [linkedin.com/in/uriel-pv](https://linkedin.com/in/uriel-pv)