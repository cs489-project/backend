from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from db.models import User, JobRequest, AuthStage, Role, JobRequestState, Report, ReportState, Comment
from api.user import hash_password
from json import dumps

def seed_users(session: Session):
    users = [
        {'name': 'Test Org 1', 'email': 'testorg1@dummy', 'password': 'password', 'salt': '', 'totp_secret': '', 'role': Role.ORGANIZATION, 'md': dumps({'approved': True, 'logo_url': 'example.com'})},
        {'name': 'Test Org 2', 'email': 'testorg2@dummy', 'password': 'password', 'salt': '', 'totp_secret': '', 'role': Role.ORGANIZATION, 'md': dumps({'approved': True, 'logo_url': 'example.com'})},
        {'name': 'Shariiii', 'email': 'shari@bytebreaker', 'password': 'password123', 'salt': '', 'totp_secret': '', 'role': Role.RESEARCHER, 'md': '{}'},
        {'name': 'admin', 'email': 'admin@bytebreaker', 'password': 'password123', 'salt': '', 'totp_secret': '', 'role': Role.ADMIN, 'md': '{}'},
        {'name': 'Hackermans', 'email': 'hackermans@bytebreaker', 'password': 'password123', 'salt': '', 'totp_secret': '', 'role': Role.RESEARCHER, 'md': '{}'},
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
        {'title': 'First request', 'summary': 'This is the summary', 'description': '# Title\n\n This is a test', 'organization_id': 1, 'state': JobRequestState.APPROVED, 'disclosure_policy_url': 'example.com', 'tags': dumps(['tag1', 't2'])},
        {'title': 'Second request', 'summary': 'This is the summary', 'description': '# Title\n\n This is a test', 'organization_id': 1, 'state': JobRequestState.ARCHIVED, 'disclosure_policy_url': 'example.com', 'tags': dumps(['tag1', 't2'])},
        {'title': 'Third request', 'summary': 'This is the summary', 'description': '# Title\n\n This is a test', 'organization_id': 2, 'state': JobRequestState.APPROVED, 'disclosure_policy_url': 'example.com', 'tags': dumps(['tag1', 't2'])}
    ]

    try:
        for r in requests:
            session.add(JobRequest(**r))
        session.commit()
    except:
        print('Error: Could not seed test request data')

def seed_reports(session: Session):
    reports = [
        {'content': 'This is a report', 'user_has_unread': True, 'org_has_unread': True, 'status': ReportState.SUBMITTED, 'user_id': 3, 'job_request_id': 1},
        {'content': 'This is a report', 'user_has_unread': True, 'org_has_unread': True, 'status': ReportState.ACCEPTED, 'user_id': 5, 'job_request_id': 1},
        {'content': 'This is a report', 'user_has_unread': True, 'org_has_unread': True, 'status': ReportState.ACCEPTED, 'user_id': 5, 'job_request_id': 3}
    ]

    try:
        for r in reports:
            session.add(Report(**r))
        session.commit()
    except:
        print('Error: Could not seed test request data')

def seed_comments(session: Session):
    comments = [
        {'content': 'This is the first comment by the researcher', 'user_id': 5, 'report_id': 2},
        {'content': 'This is the first comment by the organization', 'user_id': 1, 'report_id': 2},
        {'content': 'This is the second comment by the researcher', 'user_id': 5, 'report_id': 2}
    ]

    try:
        for r in comments:
            session.add(Comment(**r))
        session.commit()
    except:
        print('Error: Could not seed test request data')

def seed_all(session: Session):
    seed_users(session)
    seed_requests(session)
    seed_reports(session)
    seed_comments(session)
