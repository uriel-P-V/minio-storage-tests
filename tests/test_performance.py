import io
import pytest

SAMPLE_DATA = b"x" * 1024  # 1KB

@pytest.mark.regression
def test_bucket_creation_performance(benchmark, minio_client):
    """Bucket creation should complete under 500ms"""
    bucket_name = "perf-bucket"

    def create_and_delete():
        minio_client.make_bucket(bucket_name)
        minio_client.remove_bucket(bucket_name)

    benchmark(create_and_delete)
    assert benchmark.stats["mean"] < 0.5

@pytest.mark.regression
def test_object_upload_performance(benchmark, minio_client, test_bucket):
    """1KB object upload should complete under 200ms"""
    counter = {"n": 0}

    def upload():
        counter["n"] += 1
        name = f"perf-{counter['n']}.txt"
        minio_client.put_object(
            test_bucket, name,
            io.BytesIO(SAMPLE_DATA),
            len(SAMPLE_DATA)
        )

    benchmark(upload)
    assert benchmark.stats["mean"] < 0.2

@pytest.mark.regression
def test_object_download_performance(benchmark, minio_client, test_bucket):
    """1KB object download should complete under 200ms"""
    minio_client.put_object(
        test_bucket, "perf-download.txt",
        io.BytesIO(SAMPLE_DATA),
        len(SAMPLE_DATA)
    )

    def download():
        response = minio_client.get_object(test_bucket, "perf-download.txt")
        response.read()

    benchmark(download)
    assert benchmark.stats["mean"] < 0.2