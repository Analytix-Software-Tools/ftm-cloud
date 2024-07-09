from ftmcloud.core.config.config import Settings
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


def has_elevated_privileges(user: User):
    """
    Ascertains whether the specified user has heightened
    privileges or not.

    :param user:
    :return: a boolean representing whether the user's privileges are heightened
    """
    return user.privilegePid == Settings().SUPERUSER_PRIVILEGE
