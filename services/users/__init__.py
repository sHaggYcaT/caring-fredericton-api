from core.db import get_filter_conditions
from core.db.users import check_for_duplicate_name
from core.db.user.model import UserModel 
from webargs import missing


def build_filter_condition(**kwargs):
    conditions = []

    #is_verified = kwargs['is_verified']
    #if is_verified is not missing:
    #    conditions.append(UserModel.is_verified == is_verified)

    return get_filter_conditions(conditions)

