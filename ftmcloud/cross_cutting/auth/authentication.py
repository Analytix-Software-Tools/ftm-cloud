from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext

from ftmcloud.core.exception.exception import FtmException
from ftmcloud.domains.users.services.user_services import user_collection

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
