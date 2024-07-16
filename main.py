import os

from db_config import SessionLocal
import sentry_sdk
from controllers import authenticate_user, view_clients, view_contracts, view_events, manage_collaborators
from controllers import create_client_menu, update_client_menu, delete_client_menu
from controllers import create_contract_menu, update_contract_menu, delete_contract_menu
from controllers import create_event_menu, update_event_menu, delete_event_menu
from controllers import view_contracts_by_status, view_unassigned_event, view_event_support_id
from views import display_menu, prompt_login
from permissions import has_permission

dsn_adress = os.environ['dsn']
# Initialize Sentry
sentry_sdk.init(
    dsn_adress,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def main():
    db = SessionLocal()
    while True:
        username, password = prompt_login()
        try:
            user = authenticate_user(db, username, password)
        except ValueError as e:
            print(f"An error occurred: {e}")
            continue
        if user:
            while True:
                display_menu(user)
                choice = input("Select an option: ")

                try:
                    if choice == '1':
                        view_clients(db)
                    elif choice == '2':
                        view_contracts(db)
                    elif choice == '3':
                        view_events(db)
                    elif choice == '4' and has_permission(user, 'create', 'collaborator'):
                        manage_collaborators(db)
                    elif choice == '5' and has_permission(user, 'create', 'client'):
                        create_client_menu(db,user.id)
                    elif choice == '6' and has_permission(user, 'create', 'contract'):
                        create_contract_menu(db)
                    elif choice == '7' and has_permission(user, 'create', 'event'):
                        create_event_menu(db)
                    elif choice == '8':
                        view_unassigned_event(db)
                    elif choice == '9':
                        view_event_support_id(db)
                    elif choice == '10':
                        view_contracts_by_status(db)
                    elif choice == '11' and has_permission(user, 'update', 'client'):
                        update_client_menu(db)
                    elif choice == '12' and has_permission(user, 'delete', 'client'):
                        delete_client_menu(db)
                    elif choice == '13' and has_permission(user, 'update', 'contract'):
                        update_contract_menu(db)
                    elif choice == '14' and has_permission(user, 'delete', 'contract'):
                        delete_contract_menu(db)
                    elif choice == '15' and has_permission(user, 'update', 'event'):
                        update_event_menu(db)
                    elif choice == '16' and has_permission(user, 'delete', 'event'):
                        delete_event_menu(db)
                    elif choice == '17':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice or you do not have the required permissions. Please try again.")
                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    print(f"An error occurred: {e}")
        else:
            print("Invalid username or password. Please try again.")


if __name__ == "__main__":
    main()
