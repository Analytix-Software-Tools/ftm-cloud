from fastapi import HTTPException

from crosscutting.service import Service
from models.attribute import Attribute


class AttributesService(Service):

    def __init__(self):
        super(AttributesService, self).__init__(collection=Attribute)

    async def add_document(self, new_attribute: Attribute):
        attribute_exists = await self.find_one(
            {"name": new_attribute.name})
        if attribute_exists:
            raise HTTPException(
                status_code=409,
                detail="An attribute already exists by that name."
            )
        return await super(AttributesService, self).add_document(new_document=new_attribute)
