from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    team = Column(String, nullable=False, default='MANAGEMENT')
    hashed_password = Column(String, nullable=False)

    def __init__(self, username, password, phone=None, mobile=None, team='MANAGEMENT'):
        self.username = username
        self.phone = phone
        self.mobile = mobile
        self.team = team
        self.hashed_password = self.get_password_hash(password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def save(self, db_session):
        db_session.add(self)
        db_session.commit()

    def __str__(self):
        return f"{self.username} ({self.team})"


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sales_contact_id = Column(Integer, ForeignKey('users.id'))


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    sales_contact_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    status = Column(Boolean, default=False)


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    event_name = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client_contact = Column(String(100), nullable=False)
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    support_contact_id = Column(Integer, ForeignKey('users.id'))
    location = Column(String(200), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)





