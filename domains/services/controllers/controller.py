from fastapi import Body, APIRouter, HTTPException
from pydantic.validators import List

from crosscutting.exception import default_exception_list
from domains.services.services.services_service import ServicesService

from models.patchdocument import PatchDocument
from models.response import Response, ResponseWithHttpInfo
from models.service import Service

router = APIRouter()


@router.post("/", response_model=Service, response_description="Successfully registered service.",
             responses=default_exception_list)
async def add_service(new_service: Service = Body(...)):
    """Registers a new service within the space.
    """
    services_service = ServicesService()
    new_service = await services_service.add_document(new_service)
    return new_service


@router.get("/", response_description="Services retrieved", response_model=Response[Service],
            responses=default_exception_list)
async def get_services(q: str | None = None, limit: int | None = None, offset: int | None = None,
                       sort: str | None = None, includeTotals: bool | None = None):
    """Gets all services using the user defined parameters.
    """
    services_service = ServicesService()
    services = await services_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    headers = {}
    if includeTotals is not None:
        headers = {"X-Total-Count": str(await services_service.total(q))}
    return ResponseWithHttpInfo(data=services,
                                model=Service,
                                description="Services retrieved successfully.",
                                headers=headers)


@router.get("/{pid}", response_description="Service data retrieved", response_model=Response[Service],
            responses=default_exception_list)
async def get_service(pid: str):
    """Retrieves a service by ID.
    """
    services_service = ServicesService()
    service_exists = await services_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Service retrieved.',
                    data=[service_exists])


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched service.",
              responses=default_exception_list)
async def patch_service(pid: str, patch_list: List[PatchDocument] = Body(...)):
    """Patches a service within the space.
    """
    services_service = ServicesService()
    await services_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Service patched successfully.")


@router.delete("/{pid}", response_description="Service successfully deleted.", response_model=Response,
               responses=default_exception_list)
async def delete_service(pid: str):
    """Deletes a service.
    """
    services_service = ServicesService()
    await services_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Service deleted.")
