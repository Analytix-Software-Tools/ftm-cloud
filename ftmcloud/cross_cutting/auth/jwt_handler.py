import time

import jwt
from ftmcloud.domains.organizations.services.organization_services import OrganizationsService

from ftmcloud.core.config.config import Settings
from ftmcloud.domains.privileges.services.privilege_services import PrivilegesService
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.models.response import LoginResponse
from ftmcloud.domains.users.models.models import User

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
        'iss': 'com.analytics-software.api',
        'sub': user.pid,
        'exp': now + 2400,
        'iat': now,
        'permissions': role.permissions,
        'privilegeName': role.name,
        'orgPid': user.organizationPid
    }

    signed_jwt = jwt.encode(payload, secret_key, algorithm="HS256")

    return LoginResponse(accessToken=signed_jwt)


def decode_jwt(token: str, alg="HS256", options=None) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=[alg], options=options)
    return decoded_token if decoded_token['exp'] >= time.time() else {}


def construct_user_from_aad_token(token: str) -> User:
    decode_token = decode_jwt(token=token, alg="RS256", options={"verify_signature": False})
    if (
        "name" in decode_token and
        "unique_name" in decode_token
    ):
        first_name = decode_token["given_name"]
        last_name = decode_token["family_name"]
        return User(
            email=decode_token["unique_name"],
            firstName=first_name,
            lastName=last_name,
            organizationPid="",
            password=""
        )
    else:
        raise FtmException("error.user.InvalidToken")
