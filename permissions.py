from models import User


def has_permission(user: User, action: str, resource: str, obj=None) -> bool:
    if user.team == 'MANAGEMENT':
        return has_management_permission(action, resource, obj)
    elif user.team == 'SALES':
        return has_sales_permission(user, action, resource, obj)
    elif user.team == 'SUPPORT':
        return has_support_permission(user, action, resource, obj)
    return False


def has_management_permission(action: str, resource: str, obj=None) -> bool:
    if resource == 'collaborator' and action in ['create', 'update', 'delete']:
        return True
    if resource == 'contract' and action in ['create', 'update']:
        return True
    if resource == 'event' and action in ['update']:
        return True
    return False


def has_sales_permission(user: User, action: str, resource: str, obj=None) -> bool:
    if resource == 'client' and action == 'create':
        return True
    if resource == 'client' and action == 'update':
        return obj and obj.sales_contact_id == user.id
    if resource == 'contract' and action in ['create', 'update']:
        return obj and obj.client.sales_contact_id == user.id
    if resource == 'event' and action == 'create':
        return True
    return False


def has_support_permission(user: User, action: str, resource: str, obj=None) -> bool:
    if resource == 'event' and action == 'update':
        return obj and obj.support_contact_id == user.id
    if resource == 'event' and action == 'read':
        return obj and obj.support_contact_id == user.id
    return False


def can_view_unassigned_events(user: User) -> bool:
    return user.team in ['MANAGEMENT', 'SUPPORT']
