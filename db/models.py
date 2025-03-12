from enum import Enum
from db.connection import db
from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey
from sqlalchemy import String
from datetime import datetime
from typing import Optional, List

class BaseModel(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=db.func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=db.func.now(), server_onupdate=db.func.now())


class AuthStage(Enum):
    PASSWORD = 'password'
    MFA = 'mfa'
    EMAIL_VERIFIED = 'email_verified'

class Role(Enum):
    ADMIN = 'admin'
    RESEARCHER = 'researcher'
    ORGANIZATION = 'organization'

class User(BaseModel):
    __tablename__ = 'users'
    
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()
    totp_secret: Mapped[Optional[str]] = mapped_column()
    auth_stage: Mapped[AuthStage] = mapped_column(default=AuthStage.PASSWORD)
    role: Mapped[Role] = mapped_column()

    # relationships
    reports: Mapped[List["Report"]] = relationship('Report', back_populates='user')
    comments: Mapped[List["Comment"]] = relationship('Comment', back_populates='user')


class Report(BaseModel):
    __tablename__ = 'reports'
    

    # relationships
    comments: Mapped[List["Comment"]] = relationship('Comment', back_populates='report')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship('User', back_populates='reports')

    job_request_id: Mapped[int] = mapped_column(ForeignKey('job_requests.id'))
    job_request: Mapped["JobRequest"] = relationship('JobRequest', back_populates='report')

class Comment(BaseModel):
    __tablename__ = 'comments'

    # other fields

    # relationships
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship('User', back_populates='comments')

    report_id: Mapped[int] = mapped_column(ForeignKey('reports.id'))
    report: Mapped["Report"] = relationship('Report', back_populates='comments')

class JobRequest(BaseModel):
    __tablename__ = 'job_requests'

    # other fields

    # relationships
    report: Mapped["Report"] = relationship('Report', back_populates='job_request')

    organization_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    organization: Mapped["User"] = relationship('User', back_populates='job_requests')
