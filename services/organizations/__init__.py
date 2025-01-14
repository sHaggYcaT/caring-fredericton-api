from core.db import get_filter_condition
from core.db.organizations import check_for_duplicate_name
from core.db.organizations.model import OrganizationModel
from core.db.users.model import UserModel


def build_scan_condition(**kwargs):
    conditions = []

    is_verified = kwargs.get('is_verified')
    if is_verified is not None:
        conditions.append(OrganizationModel.is_verified == is_verified)

    return get_filter_condition(conditions)


def build_verify_organization_actions(is_verified):
    return [OrganizationModel.is_verified.set(is_verified)]


def build_user_organization_actions(organization):
    return [UserModel.organization_id.set(organization.id),
            UserModel.organization_name.set(organization.name)]


def build_update_actions(organization, **kwargs):
    actions = []

    name = kwargs.get('name')
    if name and name != organization.name:
        check_for_duplicate_name(name)
        actions.append(OrganizationModel.name.set(name))
        actions.append(OrganizationModel.search_name.set(name.lower()))

    email = kwargs.get('email')
    if email and email != organization.email:
        actions.append(OrganizationModel.email.set(email))

    phone = kwargs.get('phone')
    if phone and phone != organization.phone:
        actions.append(OrganizationModel.phone.set(phone))

    address = kwargs.get('address')
    if address and address != organization.address:
        actions.append(OrganizationModel.address.set(address))

    return actions
