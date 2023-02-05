from fastapi import APIRouter

from ftmcloud.models.privilege import Privilege
from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.api.domains.privileges.services.privilege_services import PrivilegesService

router = APIRouter()


@router.get("/{pid}", response_description="Privilege data retrieved", response_model=Response[Privilege])
async def get_privilege(pid: str):
    """Retrieves a privilege by ID.
    """
    privilege_service = PrivilegesService()
    privilege = await privilege_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='User retrieved.', data=[privilege])


@router.get("/", response_description="Privileges retrieved", response_model=Response[Privilege])
async def get_privileges(q: str | None = None, limit: int | None = None, offset: int | None = None, sort: str | None = None,
                    includeTotals: bool | None = None):
    """Gets all privileges using the user defined parameters.
    """
    privilege_service = PrivilegesService()
    privileges = await privilege_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    headers = {}
    if includeTotals is not None:
        headers = {"X-Total-Count": str(await privilege_service.total(q=q))}
    return ResponseWithHttpInfo(status_code=200,
                                response_type='success',
                                model=Privilege,
                                description="Privileges retrieved successfully.",
                                data=privileges,
                                headers=headers)
