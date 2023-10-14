from fastapi import Body, APIRouter, Depends
from pydantic.validators import List

from ftmcloud.common.auth.jwt_bearer import get_user_token
from ftmcloud.core.exception.exception import default_exception_list, FtmException
from ftmcloud.api.domains.privileges.services.privilege_services import PrivilegesService
from ftmcloud.api.domains.organizations.services.organization_services import OrganizationsService
from ftmcloud.models.patchdocument import PatchDocument
from ftmcloud.models.response import Response, LoginResponse, ResponseWithHttpInfo
from ftmcloud.models.domains.users.user import User, UserResponse, UserSignIn, UserProfile
from ftmcloud.api.domains.users.services.user_services import UserService
from ftmcloud.common.views.views import controller
from ftmcloud.core.config.config import Settings

router = APIRouter()


@controller(router)
class UsersController:

    settings = Settings()

    @router.post("/login", response_model=LoginResponse, responses=default_exception_list)
    async def login_user(self, credentials: UserSignIn = Body(...)):
        """Signs a user in using their provided credentials.
        """
        if self.settings.AUTH_METHOD != "mongo":
            raise FtmException("error.user.AuthenticationMethodDisabled")
        user_service = UserService()
        return await user_service.login_user(credentials=credentials)

    @router.post("/login/sso", response_model=LoginResponse, responses=default_exception_list)
    async def login_user_sso(self, token: str):
        """Login user with a token from AAD.
        """
        if self.settings.AUTH_METHOD != "azure":
            raise FtmException("error.user.AuthenticationMethodDisabled")
        user_service = UserService()
        user_token = await user_service.login_user_azure_ad(token=token)
        return LoginResponse(accessToken=user_token)

    @router.post("/", response_model=UserResponse, response_description="Successfully registered user.",
                 responses=default_exception_list)
    async def signup_user(self, new_user: User = Body(...)):
        """Registers a new user within the space.
        """
        user_services = UserService()
        user = await user_services.validate_new_user(user=new_user)
        privilege_service = PrivilegesService()
        organization_service = OrganizationsService()
        await privilege_service.validate_exists(pid=user.privilegePid)
        await organization_service.validate_exists(pid=user.organizationPid)
        await user_services.add_document(user)
        return new_user

    @router.patch("/{pid}", response_model=Response, response_description="Successfully patched user.",
                  responses=default_exception_list)
    async def patch_user(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches a user within the space.
        """
        user_service = UserService()
        await user_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="User patched successfully.")

    @router.get("/", response_description="Users retrieved", response_model=Response[UserResponse],
                responses=default_exception_list)
    async def get_users(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                        sort: str | None = None, includeTotals: bool | None = None):
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
    async def get_user(self, pid: str):
        """Retrieves a user by ID.
        """
        user_services = UserService()
        user = await user_services.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='User retrieved.', data=[user])

    @router.delete("/{pid}", response_description="User successfully deleted.", response_model=Response,
                   responses=default_exception_list)
    async def delete_user(self, pid: str):
        """Deletes a user.
        """
        user_services = UserService()
        await user_services.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="User deleted.")

    @router.post('/profile', response_description="User profile successfully retrieved.",
                 response_model=Response[UserProfile], responses=default_exception_list)
    async def users_profile(self, token: dict = Depends(get_user_token)):
        """Retrieves the current user's profile given their access token.
        """
        user_service = UserService()
        user_profile = await user_service.users_profile(token=token)
        return Response(status_code=200, response_type="success", description="User profile retrieved.",
                        data=[user_profile])

    @router.patch('/profile/modify', response_description="User profile successfully modified.",
                  response_model=Response, responses=default_exception_list)
    async def patch_users_profile(self, patch_list: List[PatchDocument], token: dict = Depends(get_user_token)):
        user_service = UserService()
        await user_service.patch_users_profile(pid=token['sub'], patch_document_list=patch_list)
        return Response(status_code=204, response_type="success", description="User profile modified.")
