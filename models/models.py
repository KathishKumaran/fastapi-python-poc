# models/models.py
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    encrypted_password = Column(String)
    access_token = Column(String)
    is_currently_logged_in = Column(Boolean, default=False)
    current_sign_in_at = Column(DateTime(timezone=True), server_default=func.now())
    last_sign_in_at = Column(DateTime(timezone=True))
    current_sign_in_ip = Column(String)
    last_sign_in_ip = Column(String)
    confirmed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


