from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from db.models import User

def seed_users(session: Session):
    ...

def seed_all(session: Session):
    seed_users(session)
