from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext

from crosscutting.error.exception import FtmException
from domains.users.services.user_services import user_collection

security = HTTPBasic()
hash_helper = CryptContext(schemes=["bcrypt"])


async def validate_login(credentials: HTTPBasicCredentials = Depends(security)):
    admin = user_collection.find_one({"email": credentials.username})
    if admin:
        password = hash_helper.verify(credentials.password, admin['password'])
        if not password:
            raise FtmException('error.user.InvalidCredentials')
        return True
    return False


async def init_controller(permissions: str):
    """Initialize the controller by cross-referencing the user
    permissions with those in the array. If the user does not
    have the right permissions, raises an HTTPException stating
    so.

    :param permissions:
    :return: None
    """
    pass
