from sqlalchemy.orm import Session
from models import Client, Contract, Event, User


# User queries
def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    return db.query(User).all()


def update_user(db: Session, user: User, updates: dict):
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


# Client queries
def get_all_clients(db: Session):
    return db.query(Client).all()


def get_client_by_id(db: Session, client_id: int) -> Client:
    return db.query(Client).filter(Client.id == client_id).first()


def create_client(db: Session, client: Client):
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db: Session, client: Client, updates: dict):
    for key, value in updates.items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client: Client):
    db.delete(client)
    db.commit()


# Contract queries
def get_all_contracts(db: Session):
    return db.query(Contract).all()


def get_contract_by_id(db: Session, contract_id: int) -> Contract:
    return db.query(Contract).filter(Contract.id == contract_id).first()


def create_contract(db: Session, contract: Contract):
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def update_contract(db: Session, contract: Contract, updates: dict):
    for key, value in updates.items():
        setattr(contract, key, value)
    db.commit()
    db.refresh(contract)
    return contract


def delete_contract(db: Session, contract: Contract):
    db.delete(contract)
    db.commit()


# Event queries
def get_all_events(db: Session):
    return db.query(Event).all()


def get_event_by_id(db: Session, event_id: int) -> Event:
    return db.query(Event).filter(Event.id == event_id).first()


def create_event(db: Session, event: Event):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event: Event, updates: dict):
    for key, value in updates.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event: Event):
    db.delete(event)
    db.commit()


# Filtering queries
def get_unassigned_events(db: Session):
    return db.query(Event).filter(Event.support_contact_id == None).all()


def get_events_by_support_contact(db: Session, support_contact_id: int):
    return db.query(Event).filter(Event.support_contact_id == support_contact_id).all()


def get_contracts_by_signed_status(db: Session, signed: bool):
    return db.query(Contract).filter(Contract.status == signed).all()
