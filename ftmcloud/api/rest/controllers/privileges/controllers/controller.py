from fastapi import APIRouter

from ftmcloud.domains.privileges.models.models import Privilege
from ftmcloud.cross_cutting.models.response import Response, ResponseWithHttpInfo
from ftmcloud.domains.privileges.services.privilege_services import PrivilegesService
from ftmcloud.cross_cutting.views.views import controller

router = APIRouter()


@controller(router)
class PrivilegesController:

    @router.get("/{pid}", response_description="Privilege data retrieved", response_model=Response[Privilege])
    async def get_privilege(self, pid: str):
        """Retrieves a privilege by ID.
        """
        privilege_service = PrivilegesService()
        privilege = await privilege_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='User retrieved.', data=[privilege])

    @router.get("/", response_description="Privileges retrieved", response_model=Response[Privilege])
    async def get_privileges(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None,
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
