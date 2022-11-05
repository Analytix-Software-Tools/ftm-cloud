from fastapi import Body, APIRouter, HTTPException
from pydantic.validators import List

from crosscutting.exception import default_exception_list
from domains.service_classifications.services.service_classification_services import ServiceClassificationsService

from models.patchdocument import PatchDocument
from models.response import Response, ResponseWithHttpInfo
from models.service_classifications import ServiceClassification

router = APIRouter()


@router.post("/", response_model=ServiceClassification, response_description="Successfully registered service classification.",
             responses=default_exception_list)
async def add_service_classification(new_service_classification: ServiceClassification = Body(...)):
    """Registers a new service classification within the space.
    """
    service_classifications_service = ServiceClassificationsService()
    new_service_classification = await service_classifications_service.add_document(new_service_classification)
    return new_service_classification


@router.get("/", response_description="Service classifications retrieved", response_model=Response[ServiceClassification],
            responses=default_exception_list)
async def get_service_classifications(q: str | None = None, limit: int | None = None, offset: int | None = None,
                                      sort: str | None = None, includeTotals: bool | None = None):
    """Gets all industries using the user defined parameters.
    """
    service_classifications_service = ServiceClassificationsService()
    industries = await service_classifications_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    headers = {}
    if includeTotals is not None:
        headers = {"X-Total-Count": str(await service_classifications_service.total(q))}
    return ResponseWithHttpInfo(data=industries,
                                model=ServiceClassification,
                                description="Service classifications retrieved successfully.",
                                headers=headers)


@router.get("/{pid}", response_description="Service classification data retrieved", response_model=Response[ServiceClassification],
            responses=default_exception_list)
async def get_service_classification(pid: str):
    """Retrieves a service classification by ID.
    """
    service_classifications_service = ServiceClassificationsService()
    service_classification_exists = await service_classifications_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Service classification retrieved.',
                    data=[service_classification_exists])


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched service classification.",
              responses=default_exception_list)
async def patch_service_classification(pid: str, patch_list: List[PatchDocument] = Body(...)):
    """Patches a service classification within the space.
    """
    service_classifications_service = ServiceClassificationsService()
    await service_classifications_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Service classification patched successfully.")


@router.delete("/{pid}", response_description="Service classification successfully deleted.", response_model=Response,
               responses=default_exception_list)
async def delete_service_classification(pid: str):
    """Deletes a service classification.
    """
    service_classification_service = ServiceClassificationsService()
    child_service_classifications = await service_classification_service.get_all(additional_filters={"parentServiceClassificationPid": pid})
    if len(child_service_classifications) > 0:
        message = "Please remove or de-associate the following child service classifications before deletion: "
        for i in range(0, len(child_service_classifications)):
            message += child_service_classifications[i].name
        raise HTTPException(status_code=409, detail=message)
    await service_classification_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Service classification deleted.")
