from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from minio import Minio
# import models
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@postgres:5432/postgres"

db = SQLAlchemy(app)

r = redis.Redis(host='redis', port=6379, db=0)
r.set('count', 1)

client = Minio("minio:9000",
    access_key=os.environ['MINIO_ROOT_USER'],
    secret_key=os.environ['MINIO_ROOT_PASSWORD'],
    secure=False
)

# The file to upload, change this path if needed
source_file = "requirements.txt"

# The destination bucket and filename on the MinIO server
bucket_name = "python-test-bucket"
destination_file = "requirements-uploaded.txt"

# Make the bucket if it doesn't exist.
found = client.bucket_exists(bucket_name)
if not found:
    client.make_bucket(bucket_name)
    print("Created bucket", bucket_name)
else:
    print("Bucket", bucket_name, "already exists")

# Upload the file, renaming it in the process
client.fput_object(
    bucket_name, destination_file, source_file,
)
print(
    source_file, "successfully uploaded as object",
    destination_file, "to bucket", bucket_name,
)

@app.route('/api')
def hello():
    r.incr('count')
    return f"Hello World {r.get('count')}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)

# def seed():
#     seed_users()
#     seed_orgs()

# def seed_users()
#     u = models.User(a, b, c)
#     db.session.addall([u])

with app.app_context():
    db.create_all()
    # seed()

