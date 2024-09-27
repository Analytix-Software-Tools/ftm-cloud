from fastapi import Body, APIRouter
from pydantic.validators import List

from ftmcloud.core.exception.exception import default_exception_list
from ftmcloud.domains.attributes.services.attribute_services import AttributesService

from ftmcloud.cross_cutting.models.patchdocument import PatchDocument
from ftmcloud.cross_cutting.models.response import Response, ResponseWithHttpInfo
from ftmcloud.domains.attributes.models.models import Attribute
from ftmcloud.cross_cutting.views.views import controller

router = APIRouter()


@controller(router)
class AttributesController:

    @router.post("/", response_model=Attribute, response_description="Successfully registered attribute.",
                 responses=default_exception_list)
    async def add_attribute(self, new_attribute: Attribute = Body(...)):
        """Registers a new attribute within the space.
        """
        attribute_service = AttributesService()
        new_attribute = await attribute_service.add_document(new_attribute)
        return new_attribute

    @router.get("/", response_description="Attributes retrieved", response_model=Response[Attribute],
                responses=default_exception_list)
    async def get_attributes(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None, includeTotals: bool | None = None):
        """Gets all attributes using the user defined parameters.
        """
        attributes_service = AttributesService()
        industries = await attributes_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await attributes_service.total(q))}
        return ResponseWithHttpInfo(data=industries,
                                    model=Attribute,
                                    description="Attributes retrieved successfully.",
                                    headers=headers)

    @router.get("/{pid}", response_description="Attribute data retrieved", response_model=Response[Attribute],
                responses=default_exception_list)
    async def get_attribute(self, pid: str):
        """Retrieves a attribute by ID.
        """
        attribute_service = AttributesService()
        attribute_exists = await attribute_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='Attribute retrieved.',
                        data=[attribute_exists])

    @router.patch("/{pid}", response_model=Response, response_description="Successfully patched attribute.",
                  responses=default_exception_list)
    async def patch_attribute(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches a attribute within the space.
        """
        attributes_service = AttributesService()
        await attributes_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="Attribute patched successfully.")

    @router.delete("/{pid}", response_description="Attribute successfully deleted.", response_model=Response,
                   responses=default_exception_list)
    async def delete_attribute(self, pid: str):
        """Deletes a attribute.
        """
        attributes_service = AttributesService()
        await attributes_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="Attribute deleted.")
