from ftmcloud.core.exception.exception import FtmException
from ftmcloud.core.service import Service
from ftmcloud.models.category import Category
from ftmcloud.models.product_type import ProductType


class CategoriesService(Service):

    def __init__(self):
        super(CategoriesService, self).__init__(collection=Category)

    async def add_document(self, new_category: Category):
        category_exists = await self.find_one(
            {"name": new_category.name, "isDeleted": {"$ne": "true"}})
        if category_exists:
            raise FtmException('error.category.InvalidName')
        if new_category.parentCategoryPid is not None:
            parent_category_exists = await self.find_one({"pid": new_category.parentCategoryPid, "isDeleted": {"$ne": "true"}})
            if not parent_category_exists:
                raise FtmException('error.category.NotFound', developer_message="Parent category not found!",
                                   user_message="We couldn't find the parent category you specified.")
        return await super(CategoriesService, self).add_document(new_document=new_category)

    async def patch(self, pid: str, patch_document_list: list):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == '/parentProductCategoryPid':
                exists = await self.base_model.find_one(
                    {"pid": patch_document_list[i].value, "isDeleted": {"$ne": "true"}})
                if exists is None:
                    raise FtmException('error.category.NotFound')
        return await super(CategoriesService, self).patch(pid=pid, patch_document_list=patch_document_list)

    async def delete_document(self, pid: str):
        product_types = await ProductType.find_one({"productCategoryPid": pid, "isDeleted": {"$ne": "true"}})
        if product_types is not None:
            raise FtmException('error.category.NotEmpty')
        return await super(CategoriesService, self).delete_document(pid=pid)
