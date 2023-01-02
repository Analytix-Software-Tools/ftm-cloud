from fastapi import HTTPException

from crosscutting.service import Service
from models.category import Category
from models.product_type import ProductType as ServiceModel


class CategoriesService(Service):

    def __init__(self):
        super(CategoriesService, self).__init__(collection=Category)

    async def add_document(self, new_category: Category):
        category_exists = await self.find_one(
            {"name": new_category.name})
        if category_exists:
            raise HTTPException(
                status_code=409,
                detail="A product category already exists by that name."
            )
        if new_category.parentCategoryPid is not None:
            parent_category_exists = await self.find_one({"pid": new_category.parentCategoryPid})
            if not parent_category_exists:
                raise HTTPException(
                    status_code=404,
                    detail="Parent product category not found."
                )
        return await super(CategoriesService, self).add_document(new_document=new_category)

    async def patch(self, pid: str, patch_document_list: list):
        for i in range(0, len(patch_document_list)):
            if patch_document_list[i].path == '/parentProductCategoryPid':
                exists = await self.base_model.find_one(
                    {"pid": patch_document_list[i].value, "isDeleted": {"$ne": "true"}})
                if exists is None:
                    raise HTTPException(status_code=404, detail="Product category not found.")
        return await super(CategoriesService, self).patch(pid=pid, patch_document_list=patch_document_list)

    async def delete_document(self, pid: str):
        services = await ServiceModel.find_one({"productCategoryPid": pid})
        if services is not None:
            raise HTTPException(
                status_code=409,
                detail="Please remove or de-associate all product types associated with this category."
            )
        return await super(CategoriesService, self).delete_document(pid=pid)
