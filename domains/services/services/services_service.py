from fastapi import HTTPException
from pydantic.error_wrappers import ValidationError

from crosscutting.service import Service
from models.patchdocument import PatchDocument
from models.service_classification import ServiceClassification
from models.service import Service as ServiceModel
from models.attribute import Attribute, AttributeNumberValue, AttributeDropdownValue, AttributeRangeValue, \
    AttributeValue


class ServicesService(Service):

    def __init__(self):
        super(ServicesService, self).__init__(collection=ServiceModel)

    async def add_document(self, new_service: ServiceModel):
        service_exists = await self.find_one(
            {"name": new_service.name})
        if service_exists:
            raise HTTPException(
                status_code=409,
                detail="A service already exists by that name."
            )
        if new_service.serviceClassificationPid is not None:
            service_classification_exists = await ServiceClassification.find_one({
                "pid": new_service.serviceClassificationPid})
            if service_classification_exists is None:
                raise HTTPException(
                    status_code=404,
                    detail="Service classification not found."
                )
        await self.validate_attribute_values_in_service(attribute_values=new_service.attributeValues)
        return await super(ServicesService, self).add_document(new_document=new_service)

    async def validate_attribute_values_in_service(self, attribute_values: list[AttributeValue]):
        """Validates the attribute values within the specified service. Ensures
        that the attribute value's value matches what is specified in the attribute and
        that, if applicable, the value is set to a valid dropdown option.

        :param attribute_values:
        :return: None
        """
        for i in range(0, len(attribute_values)):
            attribute = await Attribute.find_one({"pid": attribute_values[i].attributePid})
            if attribute is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attribute not found. attributeValues[{i}].attributePid"
                )
            if attribute.type == "number":
                try:
                    AttributeNumberValue.parse_obj(attribute_values[i].value)
                except:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid AttributeNumberValue on attributeValues[{i}].value"
                    )
            elif attribute.type == "dropdown":
                try:
                    AttributeDropdownValue.parse_obj(attribute_values[i].value)
                except:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid AttributeDropdownValue attributeValues[{i}].value"
                    )
            elif attribute.type == "range":
                try:
                    AttributeRangeValue.parse_obj(attribute_values[i].value)
                except:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid AttributeRangeValue on attributeValues[{i}].value"
                    )

    async def patch(self, pid: str, patch_document_list: list[PatchDocument]):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == "/attributeValues":
                await self.validate_attribute_values_in_service(attribute_values=patch_document_list[i].value)
            elif patch_document_list[i].path == "/serviceClassificationPid":
                service_classification_exists = await ServiceClassification.find_one({
                    "pid": patch_document_list[i].value})
                if service_classification_exists is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Service classification not found."
                    )
        await super(ServicesService, self).patch(pid=pid, patch_document_list=patch_document_list)
