def display_menu(user):
    print("\n===== Main Menu =====")
    print(f"Welcome, {user.username}!")
    print("1. View Clients")
    print("2. View Contracts")
    print("3. View Events")
    if user.team == 'MANAGEMENT':
        print("4. Manage Collaborators")
    if user.team == 'SALES':
        print("5. Create Client")
        print("6. Create Contract")
        print("7. Create Event")
    print("8. View Unassigned Events")
    print("9. View Events by Support Contact")
    print("10. View Contracts by Signed Status")
    if user.team == 'MANAGEMENT':
        print("11. Update Client")
        print("12. Delete Client")
        print("13. Update Contract")
        print("14. Delete Contract")
        print("15. Update Event")
        print("16. Delete Event")
    print("17. Logout")


def prompt_login():
    print("\n===== Login =====")
    username = input("Enter your username (FirstName LastName): ")
    password = input("Enter your password: ")
    return username, password


def prompt_user_info():
    username = input("Enter username: ")
    password = input("Enter password: ")
    phone = input("Enter phone (optional): ")
    mobile = input("Enter mobile (optional): ")
    team = input("Enter team (MANAGEMENT, SALES, SUPPORT): ")
    return username, password, phone, mobile, team


def display_users(users):
    print("\n=== Users ===")
    for user in users:
        print(
            f"ID: {user.id}, Username: {user.username}, Team: {user.team}, Phone: {user.phone}, Mobile: {user.mobile}")


def prompt_client_info():
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    company_name = input("Enter company name: ")
    sales_contact_id = input("Enter sales contact ID: ")
    return full_name, email, phone, company_name, sales_contact_id


def display_clients(clients):
    print("\n=== Clients ===")
    for client in clients:
        print(f"ID: {client.id}, Name: {client.full_name}, Email: {client.email}, Phone: {client.phone}, "
              f"Company: {client.company_name}, Sales Contact: {client.sales_contact_id}")


def prompt_contract_info():
    client_id = input("Enter client ID: ")
    sales_contact_id = input("Enter sales contact ID: ")
    total_amount = input("Enter total amount: ")
    amount_due = input("Enter amount due: ")
    status = input("Enter status (True/False): ").lower() == 'true'
    return client_id, sales_contact_id, total_amount, amount_due, status


def display_contracts(contracts):
    print("\n=== Contracts ===")
    for contract in contracts:
        print(f"ID: {contract.id}, Client ID: {contract.client_id}, Sales Contact ID: {contract.sales_contact_id}, "
              f"Total Amount: {contract.total_amount}, Amount Due: {contract.amount_due}, Status: {contract.status}")


def prompt_event_info():
    contract_id = input("Enter contract ID: ")
    event_name = input("Enter event name: ")
    client_id = input("Enter client ID: ")
    client_contact = input("Enter client contact: ")
    event_date_start = input("Enter event start date (YYYY-MM-DD): ")
    event_date_end = input("Enter event end date (YYYY-MM-DD): ")
    support_contact_id = input("Enter support contact ID: ")
    location = input("Enter location: ")
    attendees = int(input("Enter number of attendees: "))
    notes = input("Enter notes (optional): ")
    return contract_id, event_name, client_id, client_contact, event_date_start, event_date_end, support_contact_id, location, attendees, notes


def display_events(events):
    print("\n=== Events ===")
    for event in events:
        print(
            f"ID: {event.id}, Contract ID: {event.contract_id}, Event Name: {event.event_name}, Client ID: {event.client_id}, "
            f"Client Contact: {event.client_contact}, Event Date Start: {event.event_date_start}, "
            f"Event Date End: {event.event_date_end}, Support Contact ID: {event.support_contact_id}, "
            f"Location: {event.location}, Attendees: {event.attendees}, Notes: {event.notes}")


def display_unassigned_events(events):
    print("\n=== Unassigned Events ===")
    for event in events:
        print(f"ID: {event.id}, Event Name: {event.event_name}, Client ID: {event.client_id}, "
              f"Event Date Start: {event.event_date_start}, Event Date End: {event.event_date_end}")


def display_events_by_support_contact(events, support_contact_id):
    print(f"\n=== Events for Support Contact ID: {support_contact_id} ===")
    for event in events:
        print(f"ID: {event.id}, Event Name: {event.event_name}, Client ID: {event.client_id}, "
              f"Event Date Start: {event.event_date_start}, Event Date End: {event.event_date_end}")


def display_contracts_by_signed_status(contracts, signed):
    if signed:
        status = "Signed"
    else:
        status = "Unsigned"
    print(f"\n=== {status} Contracts ===")
    for contract in contracts:
        print(f"ID: {contract.id}, Client ID: {contract.client_id}, Total Amount: {contract.total_amount}, "
              f"Amount Due: {contract.amount_due}, Status: {contract.status}")
