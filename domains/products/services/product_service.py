from fastapi import HTTPException
from pydantic.error_wrappers import ValidationError

from crosscutting.service import Service
from models.patchdocument import PatchDocument
from models.category import Category
from models.organization import Organization
from models.product_type import ProductType
from models.product import Product
from models.attribute import Attribute, AttributeNumberValue, AttributeDropdownValue, AttributeRangeValue, \
    AttributeValue


class ProductService(Service):

    def __init__(self):
        super(ProductService, self).__init__(collection=Product)

    async def add_document(self, new_product: Product):
        product_type_exists = await self.find_one(
            {"name": new_product.name, "isDeleted": {"$ne": "true"}})
        if product_type_exists:
            raise HTTPException(
                status_code=409,
                detail="A product already exists by that name."
            )
        organization_exists = await Organization.find_one({
            "pid": new_product.organizationPid,
            "isDeleted": {"$ne": "true"}
        })
        if organization_exists is None:
            raise HTTPException(
                status_code=404,
                detail="Organization not found."
            )
        await self.validate_attribute_values_in_product(product=new_product)
        return await super(ProductService, self).add_document(new_document=new_product)

    async def validate_attribute_values_in_product(self, product: Product):
        """Validates the product's attribute values by checking against the nture of
        both the type of attribute as well as ensuring attributes from the product type
        have been populated and match the proper formatting for that attribute type.

        It is important to note that since this method handles validation against the
        product type, it also handles validation of the product type.
        """
        product_type = await ProductType.find_one({
            "pid": product.productTypePid,
            "isDeleted": {"$ne": "true"}
        })
        if product_type is None:
            raise HTTPException(
                status_code=404,
                detail="Product type not found"
            )
        product_type_attribute_pid_mapping = {}
        for value in product_type.attributeValues:
            product_type_attribute_pid_mapping[value.attributePid] = True
        attribute_values = product.attributeValues
        for i in range(0, len(attribute_values)):
            attribute = await Attribute.find_one({"pid": attribute_values[i].attributePid, "isDeleted": {"$ne": "true"}})
            if attribute_values[i].attributePid not in product_type_attribute_pid_mapping:
                raise HTTPException(
                    status_code=400,
                    detail=f"Attribute {attribute.name} does not exist on product type. attributeValues[{i}].attributePid"
                )
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
            # TODO: Need to handle checking attributeValues at this level.
            # if patch_document_list[i].path == "/attributeValues":
            #     await self.validate_attribute_values_in_product(attribute_values=patch_document_list[i].value)
            if patch_document_list[i].path == "/productTypePid":
                category_exists = await ProductType.find_one({
                    "pid": patch_document_list[i].value, "isDeleted": {"$ne": "true"}})
                if category_exists is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Product type not found."
                    )
            elif patch_document_list[i].path == "/organizationPid":
                organization_exists = await Organization.find_one({
                    "pid": patch_document_list[i].value,
                    "isDeleted": {"$ne": "true"}
                })
                if organization_exists is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Organization not found."
                    )
        await super(ProductService, self).patch(pid=pid, patch_document_list=patch_document_list)
