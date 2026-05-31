import pytest
from minio import Minio

@pytest.fixture
def minio_client():
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    return client

@pytest.fixture
def test_bucket(minio_client):
    bucket_name = "test-bucket-pytest"
    
    # Setup — corre ANTES del test
    minio_client.make_bucket(bucket_name)
    
    yield bucket_name  # ← el test corre aquí
    
    # Teardown — corre DESPUÉS del test, SIEMPRE
    # aunque el test falle
    objects = minio_client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        minio_client.remove_object(bucket_name, obj.object_name)
    minio_client.remove_bucket(bucket_name)