from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from db.models import User, JobRequest, AuthStage, Role, RequestState
from api.user import hash_password

def seed_users(session: Session):
    users = [
        {'name': 'Test Org 1', 'email': 'testorg1@dummy', 'password': 'password', 'salt': '', 'totp_secret': '', 'role': Role.ORGANIZATION},
        {'name': 'Test Org 2', 'email': 'testorg2@dummy', 'password': 'password', 'salt': '', 'totp_secret': '', 'role': Role.ORGANIZATION},
        {'name': 'Shariiii', 'email': 'shari@bytebreaker', 'password': 'password123', 'salt': '', 'totp_secret': '', 'role': Role.RESEARCHER},
    ]
    
    try:
        for u in users:
            u['password'] = hash_password(u['password'], u['salt'])
            session.add(User(**u))
        session.commit()
    except:
        print('Error: Could not seed test user data')

def seed_requests(session: Session):
    requests = [
        {'title': 'First request', 'description': '# Title\n\n This is a test', 'organization_id': 1, 'state': RequestState.APPROVED}
    ]

    try:
        for r in requests:
            session.add(JobRequest(**r))
        session.commit()
    except:
        print('Error: Could not seed test request data')

def seed_all(session: Session):
    seed_users(session)
    seed_requests(session)
