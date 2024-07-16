import re
from datetime import datetime
from sqlalchemy.orm import Session
import sentry_sdk
from models import Client, Contract, Event, User
from queries import get_all_clients, create_client, update_client, delete_client
from queries import get_all_contracts, create_contract, update_contract, delete_contract, get_contracts_by_signed_status
from queries import get_all_events, create_event, update_event, delete_event, get_unassigned_events
from queries import get_unassigned_events, get_events_by_support_contact, get_contracts_by_signed_status
from queries import get_user_by_username, create_user, get_all_users, update_user, delete_user
from views import display_menu, display_clients, display_contracts, display_events, display_unassigned_events
from views import display_events_by_support_contact, display_contracts_by_signed_status, prompt_login
from views import prompt_client_info, prompt_contract_info, prompt_event_info, prompt_user_info, display_users
from permissions import has_permission, can_view_unassigned_events


def validate_input(user_input):
    if not re.match("^[A-Za-z0-9@_.-]*$", user_input):
        raise ValueError("Invalid input!")
    return user_input


def view_unassigned_event(db: Session):
    event = get_unassigned_events(db)
    display_unassigned_events(event)
    input("rentrez une valeur pour retourner au menu ")


def view_contracts_by_status(db: Session):
    status_input = validate_input(input("enter the status of the contracts (1 for signed 2 for unsigned"))
    if status_input == '1':
        signed = True
    if status_input == '2':
        signed = False
    contract = get_contracts_by_signed_status(db, signed)
    display_contracts_by_signed_status(contract, signed)
    input("rentrez une valeur pour retourner au menu ")


def view_event_support_id(db: Session):
    support_id = int(input('enter the support id '))
    event = get_events_by_support_contact(db, support_id)
    display_events_by_support_contact(event, support_id)
    input("rentrez une valeur pour retourner au menu ")


def authenticate_user(db: Session, username: str, password: str):
    username = validate_input(username)
    password = validate_input(password)
    user = get_user_by_username(db, username)
    if user and user.verify_password(password):
        return user
    return None


def view_clients(db: Session):
    clients = get_all_clients(db)
    display_clients(clients)
    input("rentrez une valeur pour retourner au menu ")


def view_contracts(db: Session):
    contracts = get_all_contracts(db)
    display_contracts(contracts)
    input("rentrez une valeur pour retourner au menu ")


def view_events(db: Session):
    events = get_all_events(db)
    display_events(events)
    input("rentrez une valeur pour retourner au menu ")


def manage_collaborators(db: Session):
    print("\n=== Manage Collaborators ===")
    print("1. Create User")
    print("2. View Users")
    print("3. Update User")
    print("4. Delete User")
    choice = input("Select an option: ")

    if choice == '1':
        create_user_menu(db)
    elif choice == '2':
        view_users(db)
    elif choice == '3':
        update_user_menu(db)
    elif choice == '4':
        delete_user_menu(db)
    else:
        print("Invalid choice. Please try again.")
    input("Press any key to return to the main menu...")


def create_user_menu(db: Session):
    username, password, phone, mobile, team = prompt_user_info()
    username = validate_input(username)
    password = validate_input(password)
    phone = validate_input(phone)
    mobile = validate_input(mobile)
    team = validate_input(team)
    new_user = User(
        username=username,
        password=password,
        phone=phone,
        mobile=mobile,
        team=team
    )
    create_user(db, new_user)
    print("User created successfully.")
    input("Press any key to return to the main menu...")


def view_users(db: Session):
    users = get_all_users(db)
    display_users(users)
    input("Press any key to return to the main menu...")


def update_user_menu(db: Session):
    user_id = int(input("Enter user ID to update: "))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print("User not found.")
        return
    username, password, phone, mobile, team = prompt_user_info()
    updates = {
        "username": validate_input(username),
        "hashed_password": validate_input(password),
        "phone": validate_input(phone),
        "mobile": validate_input(mobile),
        "team": validate_input(team),
    }
    update_user(db, user, updates)
    print("User updated successfully.")
    input("Press any key to return to the main menu...")


def delete_user_menu(db: Session):
    user_id = int(input("Enter user ID to delete: "))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print("User not found.")
        return
    delete_user(db, user)
    print("User deleted successfully.")
    input("Press any key to return to the main menu...")


def create_client_menu(db: Session, sales_id):
    full_name, email, phone, company_name = prompt_client_info()
    full_name = validate_input(full_name)
    email = validate_input(email)
    phone = validate_input(phone)
    company_name = validate_input(company_name)
    sales_contact_id = sales_id
    new_client = Client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        sales_contact_id=sales_contact_id
    )
    create_client(db, new_client)
    print("Client created successfully.")
    input("Press any key to return to the main menu...")


def update_client_menu(db: Session):
    client_id = int(validate_input(input("Enter client ID to update: ")))
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        print("Client not found.")
        return
    full_name, email, phone, company_name, sales_contact_id = prompt_client_info()
    updates = {
        "full_name": validate_input(full_name),
        "email": validate_input(email),
        "phone": validate_input(phone),
        "company_name": validate_input(company_name),
        "sales_contact_id": validate_input(sales_contact_id),
    }
    update_client(db, client, updates)
    print("Client updated successfully.")
    input("Press any key to return to the main menu...")


def delete_client_menu(db: Session):
    client_id = int(validate_input(input("Enter client ID to delete: ")))
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        print("Client not found.")
        return
    delete_client(db, client)
    print("Client deleted successfully.")
    input("Press any key to return to the main menu...")


def create_contract_menu(db: Session):
    client_id, sales_contact_id, total_amount, amount_due, status = prompt_contract_info()
    client_id = validate_input(client_id)
    sales_contact_id = validate_input(sales_contact_id)
    total_amount = validate_input(total_amount)
    amount_due = validate_input(amount_due)
    status = validate_input(str(status))
    new_contract = Contract(
        client_id=client_id,
        sales_contact_id=sales_contact_id,
        total_amount=float(total_amount),
        amount_due=float(amount_due),
        status=status.lower() == 'true'
    )
    create_contract(db, new_contract)
    print("Contract created successfully.")
    input("Press any key to return to the main menu...")


def update_contract_menu(db: Session):
    contract_id = int(validate_input(input("Enter contract ID to update: ")))
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        print("Contract not found.")
        return
    client_id, sales_contact_id, total_amount, amount_due, status = prompt_contract_info()
    updates = {
        "client_id": validate_input(client_id),
        "sales_contact_id": validate_input(sales_contact_id),
        "total_amount": float(validate_input(total_amount)),
        "amount_due": float(validate_input(amount_due)),
        "status": validate_input(str(status)).lower() == 'true',
    }
    update_contract(db, contract, updates)
    print("Contract updated successfully.")
    input("Press any key to return to the main menu...")


def delete_contract_menu(db: Session):
    contract_id = int(validate_input(input("Enter contract ID to delete: ")))
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        print("Contract not found.")
        return
    delete_contract(db, contract)
    print("Contract deleted successfully.")
    input("Press any key to return to the main menu...")


def create_event_menu(db: Session):
    contract_id, event_name, client_id, client_contact, event_date_start, event_date_end, support_contact_id, location, attendees, notes = prompt_event_info()
    contract_id = validate_input(contract_id)
    event_name = validate_input(event_name)
    client_id = validate_input(client_id)
    client_contact = validate_input(client_contact)
    event_date_start = validate_input(event_date_start)
    event_date_end = validate_input(event_date_end)
    support_contact_id = support_contact_id
    location = validate_input(location)
    attendees = validate_input(str(attendees))
    notes = notes
    new_event = Event(
        contract_id=int(contract_id),
        event_name=event_name,
        client_id=int(client_id),
        client_contact=client_contact,
        event_date_start=datetime.strptime(event_date_start, "%Y-%m-%d"),
        event_date_end=datetime.strptime(event_date_end, "%Y-%m-%d"),
        support_contact_id=int(support_contact_id),
        location=location,
        attendees=int(attendees),
        notes=notes
    )
    create_event(db, new_event)
    print("Event created successfully.")
    input("Press any key to return to the main menu...")


def update_event_menu(db: Session):
    event_id = int(validate_input(input("Enter event ID to update: ")))
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        print("Event not found.")
        return
    contract_id, event_name, client_id, client_contact, event_date_start, event_date_end, support_contact_id, location, attendees, notes = prompt_event_info()
    updates = {
        "contract_id": int(validate_input(contract_id)),
        "event_name": validate_input(event_name),
        "client_id": int(validate_input(client_id)),
        "client_contact": validate_input(client_contact),
        "event_date_start": datetime.strptime(validate_input(event_date_start), "%Y-%m-%d"),
        "event_date_end": datetime.strptime(validate_input(event_date_end), "%Y-%m-%d"),
        "support_contact_id": int(validate_input(support_contact_id)),
        "location": validate_input(location),
        "attendees": int(validate_input(str(attendees))),
        "notes": validate_input(notes)
    }
    update_event(db, event, updates)
    print("Event updated successfully.")
    input("Press any key to return to the main menu...")


def delete_event_menu(db: Session):
    event_id = int(validate_input(input("Enter event ID to delete: ")))
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        print("Event not found.")
        return
    delete_event(db, event)
    print("Event deleted successfully.")
    input("Press any key to return to the main menu...")
