import unittest.mock as mock

from app import storage


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blobs_by_term_returns_none_when_bucket_does_not_exist(
    mock_storage_client
):
    mock_storage_client().lookup_bucket.return_value = None

    latest_blob = storage.get_latest_blobs_by_term()

    assert mock_storage_client().lookup_bucket.called is True
    assert latest_blob is None


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blobs_by_term_returns_blob_when_only_one_blob_exists(
    mock_storage_client
):
    mock_blob = mock.Mock()
    mock_blob.name = "123/4567890.json"
    mock_storage_client().lookup_bucket.return_value = "test-bucket"
    mock_storage_client().list_blobs.return_value = [mock_blob]

    latest_blobs = storage.get_latest_blobs_by_term()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().list_blobs.called is True
    assert latest_blobs[0].name == "123/4567890.json"


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blobs_by_term_returns_latest_blob_when_multiple_exist_in_the_same_term(
    mock_storage_client
):
    mock_blob_latest = mock.Mock()
    mock_blob_latest.name = "123/4567890.db"
    mock_blob_oldest = mock.Mock()
    mock_blob_oldest.name = "123/0000000.db"
    mock_storage_client().lookup_bucket.return_value = "test-bucket"
    mock_storage_client().list_blobs.return_value = [mock_blob_oldest, mock_blob_latest]

    latest_blobs = storage.get_latest_blobs_by_term()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().list_blobs.called is True
    assert len(latest_blobs) == 1
    assert latest_blobs[0].name == "123/4567890.db"


@mock.patch("google.cloud.storage.Client")
def test_get_latest_blobs_by_term_returns_latest_blob_by_term(mock_storage_client):
    mock_blob_one_latest = mock.Mock()
    mock_blob_one_latest.name = "123/4567890.db"
    mock_blob_one_oldest = mock.Mock()
    mock_blob_one_oldest.name = "123/0000000.db"
    mock_blob_two_latest = mock.Mock()
    mock_blob_two_latest.name = "100/4567890.db"
    mock_blob_two_oldest = mock.Mock()
    mock_blob_two_oldest.name = "100/0000000.db"
    mock_storage_client().lookup_bucket.return_value = "test-bucket"
    mock_storage_client().list_blobs.return_value = [
        mock_blob_one_oldest,
        mock_blob_one_latest,
        mock_blob_two_oldest,
        mock_blob_two_latest,
    ]

    latest_blobs = storage.get_latest_blobs_by_term()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().list_blobs.called is True
    assert len(latest_blobs) == 2
    assert latest_blobs[0].name == "100/4567890.db"
    assert latest_blobs[1].name == "123/4567890.db"


@mock.patch("google.cloud.storage.Client")
def test_upload_to_bucket_returns_none_when_no_bucket(mock_storage_client):
    mock_created_bucket = mock.Mock()
    mock_created_bucket.name = "test-bucket"
    mock_storage_client().lookup_bucket.return_value = None
    mock_storage_client().create_bucket.return_value = mock_created_bucket

    storage.upload_to_bucket()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().create_bucket.called is True


@mock.patch("app.storage.write_lambda_file")
@mock.patch("app.utils.generate_filename")
@mock.patch("google.cloud.storage.Client")
def test_upload_to_bucket_runs_until_end(
    mock_storage_client, mock_generate_filename, mock_write_lambda_file
):
    lookup_bucket = mock.Mock()
    lookup_bucket.name = "test-bucket"
    bucket_blob = mock.Mock()
    lookup_bucket.blob.return_value = bucket_blob
    mock_storage_client().lookup_bucket.return_value = lookup_bucket
    mock_generate_filename.return_value = "1234567890.db"

    storage.upload_to_bucket()

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().create_bucket.called is False


def test_write_lambda_file_returns_filename():
    filename = "test-filename"
    contents = "test-contents"

    with mock.patch(
        "builtins.open", new_callable=mock.mock_open()
    ) as mock_open:  # noqa: F841
        with mock.patch("json.dump") as mock_json:  # noqa: F841
            pass

    lambda_filename = storage.write_lambda_file(filename, contents)

    assert lambda_filename == "/tmp/test-filename"
