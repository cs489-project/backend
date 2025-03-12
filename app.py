from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from minio import Minio
import os

from db.connection import db, init_db
import db.models

import seed.seed_db as seed_db

def init_redis():
    # TODO: refactor into own file
    r = redis.Redis(host='redis', port=6379, db=0)
    r.set('count', 1)
    return r

def init_minio():
    # TODO: refactor into own file
    client = Minio("minio:9000",
        access_key=os.environ['MINIO_ROOT_USER'],
        secret_key=os.environ['MINIO_ROOT_PASSWORD'],
        secure=False
    )
    return client

def test_minio(minio_client: Minio):
    # The file to upload, change this path if needed
    source_file = "requirements.txt"

    # The destination bucket and filename on the MinIO server
    bucket_name = "python-test-bucket"
    destination_file = "requirements-uploaded.txt"

    # Make the bucket if it doesn't exist.
    found = minio_client.bucket_exists(bucket_name)
    if not found:
        minio_client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    minio_client.fput_object(
        bucket_name, destination_file, source_file,
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@postgres:5432/postgres"
    
    # init db and seed data
    init_db(app)
    with app.app_context():
        db.create_all()
    
    seed_db.seed_all(db)
    
    
app = create_app()
redis_client = init_redis()
minio_client = init_minio()

test_minio(minio_client)

@app.route('/api')
def hello():
    redis_client.incr('count')
    return f"Hello World {redis_client.get('count')}"
