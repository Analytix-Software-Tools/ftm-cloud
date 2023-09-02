from fastapi import Body, APIRouter
from pydantic.validators import List

from ftmcloud.core.exception.exception import default_exception_list, FtmException
from ftmcloud.api.domains.organizations.services.organization_services import OrganizationsService

from ftmcloud.models.patchdocument import PatchDocument
from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.models.domains.industries.industry import Industry
from ftmcloud.api.domains.industries.services.industry_services import IndustriesService
from ftmcloud.utils.views import controller

router = APIRouter()


@controller(router)
class IndustriesController:

    @router.post("/", response_model=Industry, response_description="Successfully registered industry.",
                 responses=default_exception_list)
    async def add_industry(self, new_industry: Industry = Body(...)):
        """Registers a new industry within the space.
        """
        industry_service = IndustriesService()
        industry_exists = await industry_service.find_one({"name": new_industry.name})
        if industry_exists:
            raise FtmException('error.industry.InvalidName')
        await industry_service.add_document(new_industry)
        return new_industry

    @router.get("/", response_description="Industries retrieved", response_model=Response[Industry],
                responses=default_exception_list)
    async def get_industries(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None, includeTotals: bool | None = None):
        """Gets all industries using the user defined parameters.
        """
        industry_service = IndustriesService()
        industries = await industry_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await industry_service.total(q))}
        return ResponseWithHttpInfo(data=industries,
                                    model=Industry,
                                    description="Industries retrieved successfully.",
                                    headers=headers)

    @router.get("/{pid}", response_description="Industry data retrieved", response_model=Response[Industry],
                responses=default_exception_list)
    async def get_industry(self, pid: str):
        """Retrieves an industry by ID.
        """
        industry_service = IndustriesService()
        industry = await industry_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='Industry retrieved.',
                        data=[industry])

    @router.patch("/{pid}", response_model=Response, response_description="Successfully patched industry.",
                  responses=default_exception_list)
    async def patch_industry(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches an industry within the space.
        """
        industy_service = IndustriesService()
        await industy_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="Industry patched successfully.")

    @router.delete("/{pid}", response_description="Industry successfully deleted.", response_model=Response,
                   responses=default_exception_list)
    async def delete_industry(self, pid: str):
        """Deletes a user.
        """
        industry_service = IndustriesService()
        organization_service = OrganizationsService()
        organizations = await organization_service.get_all(additional_filters={"industryPids": pid})
        if len(organizations) > 0:
            message = "Please remove or de-associate the following organizations before deletion: "
            for i in range(0, len(organizations)):
                message += organizations[i].name
            raise FtmException('error.industry.NotEmpty', developer_message=message, user_message=message)
        await industry_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="Industry deleted.")
