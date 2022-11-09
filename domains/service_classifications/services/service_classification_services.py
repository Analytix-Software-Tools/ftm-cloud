from fastapi import HTTPException

from crosscutting.service import Service
from models.service_classification import ServiceClassification


class ServiceClassificationsService(Service):

    def __init__(self):
        super(ServiceClassificationsService, self).__init__(collection=ServiceClassification)

    async def add_document(self, new_service_classification: ServiceClassification):
        service_classification_exists = await self.find_one(
            {"name": new_service_classification.name})
        if service_classification_exists:
            raise HTTPException(
                status_code=409,
                detail="A service classification already exists by that name."
            )
        if new_service_classification.parentServiceClassificationPid is not None:
            parent_service_classification_exists = await self.find_one({"pid": new_service_classification.parentServiceClassificationPid})
            if not parent_service_classification_exists:
                raise HTTPException(
                    status_code=404,
                    detail="Parent service classification not found."
                )
        return await super(ServiceClassificationsService, self).add_document(new_document=new_service_classification)

    async def patch(self, pid: str, patch_document_list: list):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == '/parentServiceClassificationPid':
                exists = await self.base_model.find_one(
                    {"pid": patch_document_list[i].value, "isDeleted": {"$ne": "true"}})
                if exists is None:
                    raise HTTPException(status_code=404, detail="Service classification not found.")
        await super(ServiceClassificationsService, self).patch(pid=pid, patch_document_list=patch_document_list)
