import os
from flask import Flask, request, stream_with_context, Response, send_file
from werkzeug.utils import secure_filename

STORAGE_LOCATION = os.environ["STORAGE_LOCATION"]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!\n\nI'm a Dunesea Server.\n\n"


@app.route('/api/v1/metadata/<domain>/', defaults={'backup_uuid': None})
@app.route('/api/v1/metadata/<domain>/<uuid:backup_uuid>')
def retrieve_metadata(domain, backup_uuid):
    metadata_dir = _get_metadata_directory(domain)
    if backup_uuid:
        return send_file(os.path.join(metadata_dir, str(backup_uuid) + ".metadata"))
    else:
        file_list = [os.path.join(metadata_dir, file_name) for file_name in os.listdir(metadata_dir)]
        if len(file_list):
            metadata_file = max(file_list,key=os.path.getctime)
            print("Sending file %s" % metadata_file)
            return send_file(metadata_file)
        else:
            return ("no-remote-metadata", 404)


@app.route('/api/v1/blob/<domain>/<blob_hash>')
def retrieve_backup(domain, blob_hash):
    return send_file(os.path.join(_get_blob_directory(domain), secure_filename(blob_hash)))

@app.route('/api/v1/metadata/<domain>/<uuid:backup_uuid>', methods=['POST'])
def store_metadata(domain, backup_uuid):
    with open(os.path.join(_get_metadata_directory(domain), str(backup_uuid) + ".metadata"), 'wb') as metadata_file:
        metadata_file.write(request.get_data())
    return 'ok'


@app.route('/api/v1/blob/<domain>/<blob_hash>', methods=['POST'])
def store_backup(domain, blob_hash):
    with open(os.path.join(_get_blob_directory(domain), secure_filename(blob_hash)), 'wb') as blob_file:
        blob_file.write(request.get_data())
    return 'ok'


def _get_storage_directory(domain):
    return os.path.join(STORAGE_LOCATION, secure_filename(domain))

def _get_blob_directory(domain):
    blob_dir = os.path.join(_get_storage_directory(domain), 'blob')
    os.makedirs(blob_dir, exist_ok=True)
    return blob_dir

def _get_metadata_directory(domain):
    metadata_dir = os.path.join(_get_storage_directory(domain), 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    return metadata_dir
