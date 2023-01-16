from fastapi import HTTPException
from pydantic.error_wrappers import ValidationError

from crosscutting.service import Service
from models.patchdocument import PatchDocument
from models.category import Category
from models.product_type import ProductType
from models.attribute import Attribute, AttributeBooleanValue, AttributeNumberValue, AttributeDropdownValue, AttributeRangeValue, \
    AttributeValue


class ProductTypesService(Service):

    def __init__(self):
        super(ProductTypesService, self).__init__(collection=ProductType)

    async def add_document(self, new_product_type: ProductType):
        product_type_exists = await self.find_one(
            {"name": new_product_type.name, "isDeleted": {"$ne": "true"}})
        if product_type_exists:
            raise HTTPException(
                status_code=409,
                detail="A product type already exists by that name."
            )
        if new_product_type.categoryPid is not None:
            category_exists = await Category.find_one({
                "pid": new_product_type.categoryPid, "isDeleted": {"$ne": "true"}})
            if category_exists is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product category not found."
                )
        await self.validate_attribute_values_in_product_type(attribute_values=new_product_type.attributeValues)
        return await super(ProductTypesService, self).add_document(new_document=new_product_type)

    async def validate_attribute_values_in_product_type(self, attribute_values: list[AttributeValue]):
        """Validates the attribute values within the specified product type. Ensures
        that the attribute value's value matches what is specified in the product type and
        that, if applicable, the value is set to a valid dropdown option.

        :param attribute_values:
        :return: None
        """
        for i in range(0, len(attribute_values)):
            attribute = await Attribute.find_one({"pid": attribute_values[i].attributePid, "isDeleted": {"$ne": "true"}})
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
            elif attribute.type == "boolean":
                try:
                    AttributeBooleanValue.parse_obj(attribute_values[i].value)
                except:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid AttributeBooleanValue on attributeValues[{i}].value"
                    )

    async def patch(self, pid: str, patch_document_list: list[PatchDocument]):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == "/attributeValues":
                await self.validate_attribute_values_in_product_type(attribute_values=patch_document_list[i].value)
            elif patch_document_list[i].path == "/categoryPid":
                category_exists = await Category.find_one({
                    "pid": patch_document_list[i].value,"isDeleted": {"$ne": "true"}})
                if category_exists is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Category not found."
                    )
        await super(ProductTypesService, self).patch(pid=pid, patch_document_list=patch_document_list)
