import os
from flask import Flask, request, stream_with_context, Response, send_file
from werkzeug.utils import secure_filename

STORAGE_LOCATION = os.environ("STORAGE_LOCATION")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!\n\nI'm a Dunesea Server."


@app.route('/api/v1/metadata/<domain>/', defaults={'backup_uuid: None})
@app.route('/api/v1/metadata/<domain>/<uuid:backup_uuid>')
def retrieve_metadata():
    if backup_uuid:
        send_file(open(os.path.join(_get_metadata_directory(domain), secure_filename(backup_uuid) + ".metadata"))
    else:
        send_file(
            open(
                max(
                    [os.path.join('/target/metadata', file_name) for file_name in os.listdir('/target/metadata')],
                    key=os.path.getctime
                )
            )
        )


@app.route('/api/v1/blob/<domain>/<blob_hash>')
def retrieve_backup(domain, blob_hash):
    send_file(open(os.path.join(_get_blob_directory(domain), secure_filename(blob_hash)))

@app.route('/api/v1/metadata/<domain>/<uuid:backup_uuid>')
def store_metadata(domain, blob_hash):
    with open(os.path.join(_get_metadata_directory(domain), secure_filename(backup_uuid) + ".metadata"), 'wb') as metadata_file:
        metadata_file.write(request.data)


@app.route('/api/v1/blob/<domain>/<blob_hash>', methods=['POST'])
def store_backup(domain, blob_hash):
    with open(os.path.join(_get_blob_directory(domain), secure_filename(blob_hash)), 'wb') as blob_file:
        blob_file.write(request.data)


def _get_storage_directory(domain):
    return os.path.join(STORAGE_LOCATION, secure_filename(domain))

def _get_blob_directory(domain):
    blob_dir = os.path.join(_get_storage_directory(domain), 'blob')
    os.makedirs(blob_dir)
    return blob_dir

def _get_metadata_directory(domain):
    metadata_dir = os.path.join(_get_storage_directory(domain), 'metadata')
    os.makedirs(metadata_dir)
    return metadata_dir
