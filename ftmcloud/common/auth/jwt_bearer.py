from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from ftmcloud.core.exception.exception import FtmException
from .jwt_handler import decode_jwt
from ftmcloud.models.domains.users.user import User


def _validate_org_in_payload(payload):
    """
    Validates the orgPid in the payload.
    """
    return 'orgPid' in payload and isinstance(payload['orgPid'], str)


def _validate_user_in_payload(payload):
    """
    Validate the user subscriber in the payload.
    """
    return 'sub' in payload and isinstance(payload['sub'], str)


def _validate_permissions_in_payload(payload):
    """
    Validates the permissions in the payload.
    """
    return 'permissions' in payload and isinstance(payload['permissions'], list)


def verify_jwt(jwtoken: str) -> bool:
    """
    Ensure the user's access token is valid and fields have not
    been modified.
    """
    is_token_valid: bool = True

    try:
        payload = decode_jwt(jwtoken)
    except InvalidTokenError:
        raise FtmException('error.user.InvalidToken')

    if payload:
        user_valid = _validate_user_in_payload(payload)
        org_valid = _validate_org_in_payload(payload)
        permissions_valid = _validate_permissions_in_payload(payload)
        is_token_valid = user_valid and org_valid and permissions_valid
    else:
        is_token_valid = False
    return is_token_valid


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise FtmException('error.user.InvalidToken',
                                   developer_message="Bad authentication method. Must be of type 'Bearer'!")

            if not verify_jwt(credentials.credentials):
                raise FtmException('error.user.InvalidToken', developer_message="Access token integrity is invalid!")

            await init_controller(credentials.credentials, request)

            return credentials.credentials
        else:
            raise FtmException('error.user.InvalidToken')


token_listener = JWTBearer()


async def get_user_token(token: str = Depends(token_listener)):
    """Decodes and retrieves the user's access control token. If the permissions field
    is specified, validates that the permission exists in the user's decoded ACL.
    """
    user = decode_jwt(token)
    return user


async def get_current_user(token_claims: dict = Depends(get_user_token)):
    """
    Retrieves the current user using the bearer access token claim.

    :param token_claims: the encoded token
    :return: the user, if they exist, otherwise an FtmException will be thrown
    """
    if 'sub' not in token_claims:
        raise FtmException('error.general.BadTokenIntegrity')
    user = await User.find_one({"pid": token_claims["sub"], "isDeleted": {"$ne": True}})
    if user is None:
        raise FtmException("error.user.InvalidUser")
    return user


async def init_controller(token: str, request: Request):
    """Initializes the controller by first decoding the user's access token,
    then parsing out their access control and verifying whether they have
    permission to perform the operation given their role.

    :param token: represents the token
    :param request: represents the request
    :return: None
    """
    user = decode_jwt(token)
    acl_list = user['permissions']
    route_path = request.method + ':' + str(request.url).replace(f'{str(request.base_url)}v0/', '').split('/')[0]
    if route_path not in acl_list:
        raise FtmException('error.user.InsufficientPrivileges')
