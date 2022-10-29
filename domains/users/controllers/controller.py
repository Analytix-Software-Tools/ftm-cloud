from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from pydantic.validators import List

from auth.jwt_bearer import get_user_token
from auth.jwt_handler import sign_jwt
from crosscutting.exception import default_exception_list
from domains.privileges.services.privilege_services import PrivilegesService
from domains.organizations.services.organization_services import OrganizationsService
from models.patchdocument import PatchDocument
from models.response import Response, LoginResponse, ResponseWithHttpInfo
from models.user import User, UserResponse, UserSignIn, UserProfile
from domains.users.services.user_services import UserService

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login", response_model=LoginResponse, responses=default_exception_list)
async def login_user(credentials: UserSignIn = Body(...)):
    """Signs a user in using their provided credentials.
    """
    user_service = UserService()
    return await user_service.login_user(credentials=credentials)


@router.post("/", response_model=UserResponse, response_description="Successfully registered user.",
             responses=default_exception_list)
async def signup_user(new_user: User = Body(...)):
    """Registers a new user within the space.
    """
    user_exists = await User.find_one(User.email == new_user.email, {"isDeleted": {"$ne": True}})
    if user_exists:
        raise HTTPException(
            status_code=409,
            detail="A user already exists by that email."
        )

    user_services = UserService()
    privilege_service = PrivilegesService()
    organization_service = OrganizationsService()
    await privilege_service.validate_exists(new_user.privilegePid)
    await organization_service.validate_exists(pid=new_user.organizationPid)
    new_user.password = hash_helper.encrypt(new_user.password)
    new_user = await user_services.add_document(new_user)
    return new_user


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched user.",
              responses=default_exception_list)
async def patch_user(pid: str, patch_list: List[PatchDocument] = Body(...)):
    """Patches a user within the space.
    """
    user_service = UserService()
    await user_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="User patched successfully.")


@router.get("/", response_description="Users retrieved", response_model=Response[UserResponse],
            responses=default_exception_list)
async def get_users(q: str | None = None, limit: int | None = None, offset: int | None = None, sort: str | None = None,
                    includeTotals: bool | None = None):
    """Gets all users using the user defined parameters.
    """
    user_services = UserService()
    users = await user_services.get_all(q=q, limit=limit, offset=offset, sort=sort)
    headers = {}
    if includeTotals is not None:
        headers = {"X-Total-Count": str(await user_services.total(q=q))}
    return ResponseWithHttpInfo(status_code=200,
                                response_type='success',
                                model=UserResponse,
                                description="Users retrieved successfully.",
                                data=users,
                                headers=headers)


@router.get("/{pid}", response_description="User data retrieved", response_model=Response[UserResponse],
            responses=default_exception_list)
async def get_user(pid: str):
    """Retrieves a user by ID.
    """
    user_services = UserService()
    user = await user_services.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='User retrieved.', data=[user])


@router.delete("/{pid}", response_description="User successfully deleted.", response_model=Response,
               responses=default_exception_list)
async def delete_user(pid: str):
    """Deletes a user.
    """
    user_services = UserService()
    await user_services.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="User deleted.")


@router.post('/profile', response_description="User profile successfully retrieved.",
             response_model=Response[UserProfile], responses=default_exception_list)
async def users_profile(token: str = Depends(get_user_token)):
    """Retrieves the current user's profile given their access token.
    """
    user_service = UserService()
    user_profile = await user_service.users_profile(pid=token['uid'])
    return Response(status_code=200, response_type="success", description="User profile retrieved.",
                    data=[user_profile])


@router.patch('/profile/modify', response_description="User profile successfully modified.",
              response_model=Response, responses=default_exception_list)
async def patch_users_profile(patch_list: List[PatchDocument], token: str = Depends(get_user_token)):
    user_service = UserService()
    await user_service.patch_users_profile(pid=token['uid'], patch_document_list=patch_list)
    return Response(status_code=204, response_type="success", description="User profile modified.")
