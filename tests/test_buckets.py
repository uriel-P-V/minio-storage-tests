import pytest
from minio.error import S3Error

def test_create_bucket(minio_client):
    """Bucket can be created successfully"""
    bucket_name = "bucket-create-test"
    minio_client.make_bucket(bucket_name)
    assert minio_client.bucket_exists(bucket_name)
    minio_client.remove_bucket(bucket_name)


def test_bucket_exists_after_creation(minio_client):
    """bucket_exists returns True for existing bucket"""
    bucket_name = "bucket-exists-test"
    minio_client.make_bucket(bucket_name)
    assert minio_client.bucket_exists(bucket_name) == True
    minio_client.remove_bucket(bucket_name)


def test_bucket_does_not_exist(minio_client):
    """bucket_exists returns False for non-existing bucket"""
    assert minio_client.bucket_exists("non-existing-bucket-xyz") == False


def test_list_buckets(minio_client, test_bucket):
    """Created bucket appears in list_buckets"""
    buckets = minio_client.list_buckets()
    bucket_names = [b.name for b in buckets]
    assert test_bucket in bucket_names


def test_delete_bucket(minio_client):
    """Bucket can be deleted successfully"""
    bucket_name = "bucket-delete-test"
    minio_client.make_bucket(bucket_name)
    minio_client.remove_bucket(bucket_name)
    assert minio_client.bucket_exists(bucket_name) == False


def test_create_duplicate_bucket_raises_error(minio_client):
    """Creating duplicate bucket raises S3Error"""
    bucket_name = "bucket-duplicate-test"
    minio_client.make_bucket(bucket_name)
    with pytest.raises(S3Error):
        minio_client.make_bucket(bucket_name)
    minio_client.remove_bucket(bucket_name)