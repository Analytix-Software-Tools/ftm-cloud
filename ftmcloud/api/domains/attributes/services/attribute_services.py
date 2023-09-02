from ftmcloud.core.exception.exception import FtmException
from ftmcloud.core.service import Service
from ftmcloud.models.domains.attributes.attribute import Attribute
from ftmcloud.models.domains.products.product import Product
from ftmcloud.models.domains.product_types.product_type import ProductType


class AttributesService(Service):

    def __init__(self):
        super(AttributesService, self).__init__(collection=Attribute)

    async def add_document(self, new_attribute: Attribute):
        attribute_exists = await self.find_one(
            {"name": new_attribute.name})
        if attribute_exists:
            raise FtmException('error.attribute.InvalidName')
        return await super(AttributesService, self).add_document(new_document=new_attribute)

    async def delete_document(self, pid: str):
        products = await Product.find_one({"attributeValues.attributePid": pid, "isDeleted": {"$ne": True}})
        if products is not None:
            raise FtmException('error.attribute.NotEmpty')
        product_types = await ProductType.find_one({"attributeValues.attributePid": pid, "isDeleted": {"$ne": True}})
        if product_types is not None:
            raise FtmException('error.attribute.NotEmpty')
        return await super(AttributesService, self).delete_document(pid=pid)
