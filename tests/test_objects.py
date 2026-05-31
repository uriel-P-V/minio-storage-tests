import pytest
import io
from minio.error import S3Error


SAMPLE_DATA = b"Hello from IBM Storage Test!"
SAMPLE_FILENAME = "test-file.txt"


def test_upload_object(minio_client, test_bucket):
    """Object can be uploaded to bucket"""
    minio_client.put_object(
        test_bucket,
        SAMPLE_FILENAME,
        io.BytesIO(SAMPLE_DATA),
        len(SAMPLE_DATA)
    )
    objects = list(minio_client.list_objects(test_bucket))
    object_names = [o.object_name for o in objects]
    assert SAMPLE_FILENAME in object_names


def test_download_object(minio_client, test_bucket):
    """Downloaded object content matches uploaded content"""
    minio_client.put_object(
        test_bucket,
        SAMPLE_FILENAME,
        io.BytesIO(SAMPLE_DATA),
        len(SAMPLE_DATA)
    )
    response = minio_client.get_object(test_bucket, SAMPLE_FILENAME)
    content = response.read()
    assert content == SAMPLE_DATA


def test_object_size(minio_client, test_bucket):
    """Object size matches uploaded data size"""
    minio_client.put_object(
        test_bucket,
        SAMPLE_FILENAME,
        io.BytesIO(SAMPLE_DATA),
        len(SAMPLE_DATA)
    )
    objects = list(minio_client.list_objects(test_bucket))
    obj = next(o for o in objects if o.object_name == SAMPLE_FILENAME)
    assert obj.size == len(SAMPLE_DATA)


def test_delete_object(minio_client, test_bucket):
    """Object can be deleted from bucket"""
    minio_client.put_object(
        test_bucket,
        SAMPLE_FILENAME,
        io.BytesIO(SAMPLE_DATA),
        len(SAMPLE_DATA)
    )
    minio_client.remove_object(test_bucket, SAMPLE_FILENAME)
    objects = list(minio_client.list_objects(test_bucket))
    object_names = [o.object_name for o in objects]
    assert SAMPLE_FILENAME not in object_names


def test_get_nonexistent_object_raises_error(minio_client, test_bucket):
    """Getting non-existent object raises S3Error"""
    with pytest.raises(S3Error):
        minio_client.get_object(test_bucket, "nonexistent.txt")


def test_list_multiple_objects(minio_client, test_bucket):
    """All uploaded objects appear in list"""
    files = ["file1.txt", "file2.txt", "file3.txt"]
    for f in files:
        minio_client.put_object(
            test_bucket, f,
            io.BytesIO(SAMPLE_DATA),
            len(SAMPLE_DATA)
        )
    objects = list(minio_client.list_objects(test_bucket))
    object_names = [o.object_name for o in objects]
    for f in files:
        assert f in object_names