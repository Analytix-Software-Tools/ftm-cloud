from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic.validators import List

from auth.jwt_handler import sign_jwt
from domains.users.services.user_services import UserService
from models.response import Response
from models.organization import Organization
from domains.organizations.services.organization_services import OrganizationsService

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/", response_model=Organization, response_description="Successfully registered organization.")
async def add_organization(new_organization: Organization = Body(...)):
    """Registers a new organization within the space.
    """
    organization_exists = await Organization.find_one(Organization.name == new_organization.name)
    if organization_exists:
        raise HTTPException(
            status_code=409,
            detail="An organization already exists by that name."
        )

    organization_services = OrganizationsService()
    await organization_services.add_document(new_organization)
    return new_organization


@router.get("/", response_description="Organizations retrieved", response_model=Response[Organization])
async def get_organizations(q: str | None = None, limit: int | None = None, offset: int | None = None, sort: str | None = None):
    """Gets all organizations using the user defined parameters.
    """
    organization_service = OrganizationsService()
    organizations = await organization_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    return Response(status_code=200,
                    response_type='success',
                    description="Organizations retrieved successfully.",
                    data=organizations)


@router.get("/{pid}", response_description="Organization data retrieved", response_model=Response[Organization])
async def get_organization(pid: str):
    """Retrieves an organization by ID.
    """
    organization_service = OrganizationsService()
    organization = await organization_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Organization retrieved.', data=[organization])


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched organization.")
async def patch_organization(pid: str, patch_list: List[object] = Body(...)):
    """Patches an organization within the space.
    """
    organization_service = OrganizationsService()
    await organization_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Organization patched successfully.")


@router.delete("/{pid}", response_description="Organization successfully deleted.", response_model=Response)
async def delete_organization(pid: str):
    """Deletes a user.
    """
    organization_service = OrganizationsService()
    user_service = UserService()
    users = await user_service.get_all(additional_filters={"organizationPid": pid})
    if len(users) > 0:
        raise HTTPException(status_code=409, detail="Please remove or transfer all existing users before "
                                                    "deleting this organization!")
    await organization_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Organization deleted.")
