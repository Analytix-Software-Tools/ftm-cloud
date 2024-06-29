from fastapi import Body, APIRouter
from pydantic.validators import List

from ftmcloud.core.exception.exception import default_exception_list, FtmException
from ftmcloud.domains.categories.services.category_services import CategoriesService
from ftmcloud.domains.product_types.services.product_type_service import ProductTypesService

from ftmcloud.models.patchdocument import PatchDocument
from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.models.domains.category import Category
from ftmcloud.common.views.views import controller

categories_router = APIRouter()


@controller(categories_router)
class CategoriesController:

    @categories_router.post("/", response_model=Category, response_description="Successfully registered category.",
                            responses=default_exception_list)
    async def add_category(self, new_category: Category = Body(...)):
        """Registers a new category within the space.
        """
        categories_service = CategoriesService()
        new_category = await categories_service.add_document(new_category)
        return new_category

    @categories_router.get("/", response_description="Categories retrieved", response_model=Response[Category],
                           responses=default_exception_list)
    async def get_categories(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None, includeTotals: bool | None = None):
        """Gets all categories using the user defined parameters.
        """
        categories_service = CategoriesService()
        industries = await categories_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await categories_service.total(q))}
        return ResponseWithHttpInfo(data=industries,
                                    model=Category,
                                    description="Categories retrieved successfully.",
                                    headers=headers)

    @categories_router.get("/{pid}", response_description="Category data retrieved", response_model=Response[Category],
                           responses=default_exception_list)
    async def get_category(self, pid: str):
        """Retrieves a category by ID.
        """
        categories_service = CategoriesService()
        category_exists = await categories_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='Category retrieved.',
                        data=[category_exists])

    @categories_router.patch("/{pid}", response_model=Response, response_description="Successfully patched category.",
                             responses=default_exception_list)
    async def patch_category(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches a category within the space.
        """
        categories_service = CategoriesService()
        await categories_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="Category patched successfully.")

    @categories_router.delete("/{pid}", response_description="Category successfully deleted.", response_model=Response,
                              responses=default_exception_list)
    async def delete_category(self, pid: str):
        """Deletes a category.
        """
        categories_service = CategoriesService()
        product_types_service = ProductTypesService()
        child_categories = await categories_service.get_all(additional_filters={"parentCategoryPid": pid})
        product_types = await product_types_service.get_all(additional_filters={"categoryPid": pid})
        if len(child_categories) > 0:
            message = "Please remove or de-associate the following child categories before deletion: "
            for i in range(0, len(child_categories)):
                message += child_categories[i].name
            raise FtmException('error.category.NotEmpty', developer_message=message, user_message=message)
        if len(product_types) > 0:
            message = "Please remove or de-associate the following product types before deletion: "
            for product_type in product_types:
                message += product_type.name + ' '
            raise FtmException('error.category.NotEmpty', developer_message=message, user_message=message)
        await categories_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="Category deleted.")
