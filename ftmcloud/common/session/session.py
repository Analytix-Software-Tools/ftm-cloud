from ftmcloud.core.config.config import Settings
from ftmcloud.models.domains.user import User


def has_elevated_privileges(user: User):
    """
    Ascertains whether the specified user has heightened
    privileges or not.

    :param user:
    :return: a boolean representing whether the user's privileges are heightened
    """
    return user.privilegePid == Settings().SUPERUSER_PRIVILEGE
