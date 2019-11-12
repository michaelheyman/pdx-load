import unittest.mock as mock

from app import storage


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blob_returns_none_when_bucket_does_not_exist(mock_storage_client):
    mock_storage_client().lookup_bucket.return_value = None

    latest_blob = storage.get_latest_blob()

    assert mock_storage_client().lookup_bucket.called is True
    assert latest_blob is None


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blob_returns_blob_when_only_one_blob_exists(mock_storage_client):
    mock_blob = mock.Mock()
    mock_blob.name = "1234567890.json"
    mock_storage_client().lookup_bucket.return_value = "test-bucket"
    mock_storage_client().list_blobs.return_value = [mock_blob]

    latest_blob = storage.get_latest_blob()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().list_blobs.called is True
    assert latest_blob.name == "1234567890.json"


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blob_returns_latest_blob_when_multiple_exist(mock_storage_client):
    mock_blob_latest = mock.Mock()
    mock_blob_latest.name = "1234567890.json"
    mock_blob_oldest = mock.Mock()
    mock_blob_oldest.name = "1000000000.json"
    mock_storage_client().lookup_bucket.return_value = "test-bucket"
    mock_storage_client().list_blobs.return_value = [mock_blob_oldest, mock_blob_latest]

    latest_blob = storage.get_latest_blob()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().list_blobs.called is True
    assert latest_blob.name == "1234567890.json"
