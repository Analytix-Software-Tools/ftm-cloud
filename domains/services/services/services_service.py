from fastapi import HTTPException

from crosscutting.service import Service
from models.patchdocument import PatchDocument
from models.service_classification import ServiceClassification
from models.service import Service as ServiceModel
from models.attribute import Attribute


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
        for i in range(0, len(new_service.attributeValues)):
            attribute_exists = await Attribute.find_one({"pid": new_service.attributeValues[i].attributePid})
            if attribute_exists is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attribute not found. attributeValues[{i}].attributePid"
                )
        return await super(ServicesService, self).add_document(new_document=new_service)

    async def patch(self, pid: str, patch_document_list: list[PatchDocument]):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == "/attributeValues":
                for j in range(0, len(patch_document_list[i].value)):
                    attribute_exists = await Attribute.find_one({"pid": patch_document_list[i].value[j].attributePid})
                    if attribute_exists is None:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Attribute not found on attributeValues{i}"
                        )
            elif patch_document_list[i].path == "/serviceClassificationPid":
                service_classification_exists = await ServiceClassification.find_one({"pid": patch_document_list[i].value})
                if service_classification_exists is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Service classification not found."
                    )
        await super(ServicesService, self).patch(pid=pid, patch_document_list=patch_document_list)
