from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.cross_cutting.models.patchdocument import PatchDocument
from ftmcloud.domains.organizations.models.models import Organization
from ftmcloud.domains.product_types.models.models import ProductType
from ftmcloud.domains.products.models.models import Product
from ftmcloud.domains.attributes.models.models import Attribute, AttributeBooleanValue, AttributeNumberValue, AttributeDropdownValue, AttributeRangeValue, AttributeTextValue, AttributeValue


class ProductService(Service):

    def __init__(self):
        super(ProductService, self).__init__(collection=Product)

    async def add_document(self, new_product: Product):
        product_type_exists = await self.find_one(
            {"name": new_product.name, "isDeleted": {"$ne": "true"}})
        if product_type_exists:
            raise FtmException('error.product.InvalidName')
        organization_exists = await Organization.find_one({
            "pid": new_product.organizationPid,
            "isDeleted": {"$ne": "true"}
        })
        if organization_exists is None:
            raise FtmException('error.organization.NotFound')
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
            raise FtmException('error.producttype.NotFound')
        product_type_attribute_pid_mapping = {}
        required_attribute_to_found = {}
        for value in product_type.attributeValues:
            product_type_attribute_pid_mapping[value.attributePid] = value
            if value.isRequired:
                required_attribute_to_found[value.attributePid] = False
        attribute_values = product.attributeValues
        for i in range(0, len(attribute_values)):

            try:
                attribute_value = AttributeValue.parse_obj(attribute_values[i])
            except:
                raise FtmException("error.attribute.InvalidAttributeValue")
            
            attribute = await Attribute.find_one({"pid": attribute_value.attributePid, "isDeleted": {"$ne": "true"}})

            if attribute is None:
                raise FtmException('error.attribute.NotFound',
                                   developer_message=f"Attribute not found. attributeValues[{i}].attributePid")
            if attribute_value.attributePid not in product_type_attribute_pid_mapping:
                raise FtmException('error.product.InvalidAttributeValue',
                                   developer_message=f"Attribute '{attribute.name}' does not exist on product type. attributeValues[{i}].attributePid")
            if attribute_value.attributePid in required_attribute_to_found:
                required_attribute_to_found[attribute_value.attributePid] = True
            if attribute.type == "number":
                try:
                    AttributeNumberValue.parse_obj(attribute_value.value)
                except:
                    raise FtmException('error.attribute.InvaludAttributeNumberValue',
                                       developer_message=f"Invalid AttributeNumberValue on attributeValues[{i}].value")
            elif attribute.type == "dropdown":
                try:
                    AttributeDropdownValue.parse_obj(attribute_value.value)
                except:
                    raise FtmException('error.attribute.InvalidAttributeDropdownValue',
                                       developer_message=f"Invalid AttributeDropdownValue attributeValues[{i}].value")
                if attribute_value.value.value not in product_type_attribute_pid_mapping[attribute_value.attributePid].value.options:
                    raise FtmException('error.product.InvalidAttributeValue',
                                       developer_message=f"Invalid value '{attribute_value.value.value}' not specified in product type. attributeValues[{i}].value.value")
            elif attribute.type == "text":
                try:
                    AttributeTextValue.parse_obj(attribute_value.value)
                except:
                    raise FtmException('error.attribute.InvalidAttributeTextValue',
                                       developer_message=f"Invalid AttributeTextValue attributeValues[{i}].value")
            elif attribute.type == "range":
                try:
                    AttributeRangeValue.parse_obj(attribute_value.value)
                except:
                    raise FtmException('error.attribute.InvalidAttributeRangeValue',
                                       developer_message=f"Invalid AttributeRangeValue on attributeValues[{i}].value")
            elif attribute.type == "boolean":
                try:
                    AttributeBooleanValue.parse_obj(attribute_value.value)
                except:
                    raise FtmException('error.attribute.InvalidAttributeBooleanValue',
                                       developer_message=f"Invalid AttributeBooleanValue on attributeValues[{i}].value")
        for key in required_attribute_to_found.keys():
            if required_attribute_to_found[key] == False:
                required_attr = await Attribute.find_one({"pid": key, "isDeleted": {"$ne": "true"}})
                if required_attr is None:
                    continue
                else:
                    raise FtmException('error.product.MissingRequiredAttribute',
                                       developer_message=f"Attribute '{required_attr.name}' is required for product type '{product_type.name}'.",
                                       user_message=f"Attribute '{required_attr.name}' is required for product type '{product_type.name}'.")

    async def patch(self, pid: str, patch_document_list: list[PatchDocument]):
        for i in range(0, len(patch_document_list)):
            # TODO: Need to handle checking attributeValues at this level.
            # if patch_document_list[i].path == "/attributeValues":
            #     await self.validate_attribute_values_in_product(attribute_values=patch_document_list[i].value)
            if patch_document_list[i].path == "/productTypePid":
                category_exists = await ProductType.find_one({
                    "pid": patch_document_list[i].value, "isDeleted": {"$ne": "true"}})
                if category_exists is None:
                    raise FtmException('error.category.NotFound')
            elif patch_document_list[i].path == "/organizationPid":
                organization_exists = await Organization.find_one({
                    "pid": patch_document_list[i].value,
                    "isDeleted": {"$ne": "true"}
                })
                if organization_exists is None:
                    raise FtmException('error.organization.NotFound')
        await super(ProductService, self).patch(pid=pid, patch_document_list=patch_document_list)
