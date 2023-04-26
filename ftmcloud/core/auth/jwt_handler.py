import time

import jwt
from ftmcloud.api.domains.organizations.services.organization_services import OrganizationsService

from ftmcloud.core.config.config import Settings
from ftmcloud.api.domains.privileges.services.privilege_services import PrivilegesService
from ftmcloud.models.response import LoginResponse
from ftmcloud.models.user import User


secret_key = Settings().secret_key


async def sign_jwt(user: User) -> LoginResponse:
    """Sign the JWT given the specified user. Returns a response
    containing the user's signed access token.

    :param user:
    :return:
    """
    now = int(time.time())
    role = await PrivilegesService().validate_exists(pid=user.privilegePid)
    await OrganizationsService().validate_exists(pid=user.organizationPid)

    payload = {
        'iss': 'com.analytics.ftmcloud',
        'sub': user.pid,
        'exp': now + 2400,
        'iat': now,
        'permissions': role.permissions,
        'privilegeName': role.name,
        'orgPid': user.organizationPid
    }

    signed_jwt = jwt.encode(payload, secret_key, algorithm="HS256")

    return LoginResponse(accessToken=signed_jwt)


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token['exp'] >= time.time() else {}

