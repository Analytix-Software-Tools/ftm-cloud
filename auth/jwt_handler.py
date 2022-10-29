import time
from typing import Dict

import jwt

from config.config import Settings
from domains.organizations.services.organization_services import OrganizationsService
from domains.privileges.services.privilege_services import PrivilegesService
from models.response import LoginResponse
from models.user import User


secret_key = Settings().secret_key


async def sign_jwt(user: User) -> LoginResponse:
    """Sign the JWT given the specified user. Returns a response
    containing the user's signed access token.

    :param user:
    :return:
    """
    now = time.time()
    role = await PrivilegesService().validate_exists(pid=user.privilegePid)

    payload = {
        'uid': user.pid,
        'privilege': role.routes,
        'privilegeName': role.name,
        'exp': now + 2400,
        'iat': now,
    }

    signed_jwt = jwt.encode(payload, secret_key, algorithm="HS256")

    return LoginResponse(accessToken=signed_jwt)


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token['exp'] >= time.time() else {}

