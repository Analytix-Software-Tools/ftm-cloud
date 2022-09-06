import time
from typing import Dict

import jwt

from config.config import Settings
from domains.privileges.services.privilege_services import PrivilegesService
from models.user import User


def token_response(token: str, user: User):
    return {
        "accessToken": token,
        "user": user
    }


secret_key = Settings().secret_key


async def sign_jwt(user: User) -> Dict[str, str]:
    """Sign the JWT given the specified user.

    :param user:
    :return:
    """
    now = time.time()
    role = await PrivilegesService().validate_exists(pid=user.privilegePid)

    payload = {
        'uid': user.pid,
        'privilege': role.routes,
        'exp': now + 2400,
        'iat': now,
    }
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"), user=user)


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token['exp'] >= time.time() else {}

