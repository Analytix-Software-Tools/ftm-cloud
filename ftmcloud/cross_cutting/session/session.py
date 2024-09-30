from ftmcloud.domains.privileges.models.models import Privilege
from ftmcloud.domains.users.models.models import User

import random
import string


class PasswordGenerator:
    def __init__(self, length=12):
        self.length = length
        self.characters = string.ascii_letters + string.digits + string.punctuation

    def generate(self):
        password = ''.join(random.choice(self.characters) for _ in range(self.length))
        return password


privilege_pid_to_name = {}
privilege_name_to_pid = {}

async def init_privilege_name_to_pid():
    """ Loads the mapping of privilege name to privilege pid into memory for the
    current process.

    :return:
    """
    global privilege_pid_to_name
    global privilege_name_to_pid
    privileges = await Privilege.find().to_list()
    for _privilege in privileges:
        privilege_pid_to_name[_privilege.pid] = _privilege.name
        privilege_name_to_pid[_privilege.name] = _privilege.pid


def validate_user_privilege_in_list(privilege_pid: str, privilege_names: list[str]):
    """ Validates the user privilege is in the specified list using the in-memory privilege
    name to pid mapping.

    :param privilege_pid: str
        pid of the privilege to validate
    :param privilege_names: list[str]
        list of privilege names to check against

    :return: in_list: bool
        whether the privilege is in the specified list
    """
    in_list = False
    if privilege_pid in privilege_pid_to_name:
        if privilege_pid_to_name[privilege_pid] in privilege_names:
            in_list = True

    return in_list


def get_privilege_pid_for_name(privilege_name: str):
    """ Returns the pid of the specified privilege.

    :param privilege_name: str
        name of the privilege to get the pid for

    :return: privilege_pid: str
        pid of the privilege
    """
    return privilege_name_to_pid[privilege_name]


def has_elevated_privileges(user: User):
    """
    Ascertains whether the specified user has heightened
    privileges or not.

    :param user:
    :return: a boolean representing whether the user's privileges are heightened
    """
    return validate_user_privilege_in_list(user.privilegePid, ['developer'])
