from fastapi import Body, APIRouter, HTTPException
from pydantic.validators import List

from crosscutting.exception import default_exception_list
from domains.organizations.services.organization_services import OrganizationsService

from models.patchdocument import PatchDocument
from models.response import Response, ResponseWithHttpInfo
from models.industry import Industry
from domains.industries.services.industry_services import IndustriesService

router = APIRouter()


@router.post("/", response_model=Industry, response_description="Successfully registered industry.",
             responses=default_exception_list)
async def add_industry(new_industry: Industry = Body(...)):
    """Registers a new industry within the space.
    """
    industry_exists = await Industry.find_one(Industry.name == new_industry.name)
    if industry_exists:
        raise HTTPException(
            status_code=409,
            detail="An industry already exists by that name."
        )

    industry_service = IndustriesService()
    await industry_service.add_document(new_industry)
    return new_industry


@router.get("/", response_description="Industries retrieved", response_model=Response[Industry],
            responses=default_exception_list)
async def get_industries(q: str | None = None, limit: int | None = None, offset: int | None = None,
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
async def get_industry(pid: str):
    """Retrieves an industry by ID.
    """
    industry_service = IndustriesService()
    industry = await industry_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Industry retrieved.',
                    data=[industry])


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched industry.",
              responses=default_exception_list)
async def patch_industry(pid: str, patch_list: List[PatchDocument] = Body(...)):
    """Patches an industry within the space.
    """
    industy_service = IndustriesService()
    await industy_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Industry patched successfully.")


@router.delete("/{pid}", response_description="Industry successfully deleted.", response_model=Response,
               responses=default_exception_list)
async def delete_industry(pid: str):
    """Deletes a user.
    """
    indusry_service = IndustriesService()
    organization_service = OrganizationsService()
    organizations = await organization_service.get_all(additional_filters={"industryPids": pid})
    if len(organizations) > 0:
        message = "Please remove or de-associate the following organizations before deletion: "
        for i in range(0, len(organizations)):
            message += organizations[i]['name']
        raise HTTPException(status_code=409, detail=message)
    await indusry_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Industry deleted.")
