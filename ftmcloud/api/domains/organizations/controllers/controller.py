from fastapi import Body, APIRouter, Depends
from pydantic.validators import List
from ftmcloud.core.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list, FtmException

from ftmcloud.api.domains.users.services.user_services import UserService
from ftmcloud.models.patchdocument import PatchDocument
from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.models.domains.organizations.organization import Organization
from ftmcloud.models.domains.users.user import User
from ftmcloud.api.domains.organizations.services.organization_services import OrganizationsService
from ftmcloud.common.views.views import controller

router = APIRouter()


@controller(router)
class OrganizationsController:
    current_user: User = Depends(get_current_user)

    @router.post(
        "/",
        response_model=Organization,
        response_description="Successfully registered organization.",
        responses=default_exception_list
    )
    async def add_organization(self, new_organization: Organization = Body(...)):
        """Registers a new organization within the space.
        """
        organization_services = OrganizationsService()
        organization_exists = await organization_services.find_one({"name": new_organization.name})
        if organization_exists:
            raise FtmException('error.organization.InvalidName')
        await organization_services.add_document(new_organization)
        return new_organization

    @router.get(
        "/",
        response_description="Organizations retrieved",
        response_model=Response[Organization],
        responses=default_exception_list
    )
    async def get_organizations(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                                sort: str | None = None, includeTotals: bool | None = None):
        """Gets all organizations using the user defined parameters.
        """
        organization_service = OrganizationsService()
        organizations = await organization_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await organization_service.total(q))}
        return ResponseWithHttpInfo(data=organizations,
                                    model=Organization,
                                    description="Organizations retrieved successfully.",
                                    headers=headers)

    @router.get(
        "/{pid}",
        response_description="Organization data retrieved",
        response_model=Response[Organization],
        responses=default_exception_list
    )
    async def get_organization(self, pid: str):
        """Retrieves an organization by ID.
        """
        organization_service = OrganizationsService()
        organization = await organization_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='Organization retrieved.',
                        data=[organization])

    @router.patch(
        "/{pid}",
        response_model=Response,
        response_description="Successfully patched organization.",
        responses=default_exception_list
    )
    async def patch_organization(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches an organization within the space.
        """
        organization_service = OrganizationsService()
        await organization_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="Organization patched successfully.")

    @router.patch(
        "/",
        response_model=Response,
        response_description="Successfully patched organization.",
        responses=default_exception_list
    )
    async def patch_users_organization(self,
                                       patch_document_list: List[PatchDocument] = Body(...)):
        """Patches the user's own organization, if their privileges suffice.
        """
        organization_service = OrganizationsService()
        await organization_service.patch(pid=self.current_user.organizationPid, patch_document_list=patch_document_list)
        return Response(status_code=204, response_type='success', description="Organization patched successfully.")

    @router.delete(
        "/{pid}",
        response_description="Organization successfully deleted.",
        response_model=Response,
        responses=default_exception_list
    )
    async def delete_organization(self, pid: str):
        """Deletes a user.
        """
        organization_service = OrganizationsService()
        user_service = UserService()
        users = await user_service.get_all(additional_filters={"organizationPid": pid})
        if len(users) > 0:
            raise FtmException('error.organization.NotEmpty')
        await organization_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="Organization deleted.")
