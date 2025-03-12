from flask_sqlalchemy import SQLAlchemy

def seed_users():
    ...

def seed_all(db: SQLAlchemy):
    seed_users()
    ...
