from fastapi import Body, APIRouter, Depends
from pydantic.validators import List

from ftmcloud.core.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list, FtmException
from ftmcloud.api.domains.products.services.product_service import ProductService

from ftmcloud.models.patchdocument import PatchDocument
from ftmcloud.models.domains.products.product import Product
from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.models.domains.users.user import User
from ftmcloud.utils.session import has_elevated_privileges
from ftmcloud.utils.views import controller

product_router = APIRouter()


@controller(product_router)
class ProductsController:

    @product_router.post(
        "/",
        response_model=Product,
        response_description="Successfully registered product.",
        responses=default_exception_list
    )
    async def add_product(self, new_product: Product = Body(...), current_user: User = Depends(get_current_user)):
        """
        Registers a new product within the space.
        """
        products_service = ProductService()
        if not has_elevated_privileges(user=current_user) and new_product.organizationPid != \
                current_user.organizationPid:
            raise FtmException("error.organization.NotFound")
        new_product = await products_service.add_document(new_product)
        return new_product

    @product_router.get(
        "/",
        response_description="Products retrieved",
        response_model=Response[Product],
        responses=default_exception_list
    )
    async def get_products(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                           sort: str | None = None, includeTotals: bool | None = None,
                           current_user: User = Depends(get_current_user)):
        """
        Gets all products using the user defined parameters.
        """
        products_service = ProductService()
        scope_filter = None if has_elevated_privileges(current_user) else \
            {"organizationPid": current_user.organizationPid}
        products = await products_service.get_all(q=q, limit=limit, offset=offset, sort=sort,
                                                  additional_filters=scope_filter)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await products_service.total(q, scope_filter))}
        return ResponseWithHttpInfo(data=products,
                                    model=Product,
                                    description="Products retrieved successfully.",
                                    headers=headers)

    @product_router.get(
        "/{pid}",
        response_description="Product data retrieved",
        response_model=Response[Product],
        responses=default_exception_list
    )
    async def get_product(self, pid: str, current_user: User = Depends(get_current_user)):
        """
        Retrieves a product by ID.
        """
        products_service = ProductService()
        scope_filter = None if has_elevated_privileges(current_user) else \
            {"organizationPid": current_user.organizationPid}
        product_exists = await products_service.validate_exists(pid=pid, additional_filters=scope_filter)
        if product_exists is None:
            raise FtmException("error.product.NotFound")
        return Response(status_code=200, response_type='success', description='Product retrieved.',
                        data=[product_exists])

    @product_router.patch("/{pid}", response_model=Response, response_description="Successfully patched product.",
                          responses=default_exception_list)
    async def patch_product(self, pid: str, patch_list: List[PatchDocument] = Body(...),
                            current_user: User = Depends(get_current_user)):
        """
        Patches a product within the space.
        """
        products_service = ProductService()
        if not has_elevated_privileges(current_user):
            await products_service.validate_exists(additional_filters={"organizationPid": current_user.organizationPid})
        await products_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="Product patched successfully.")

    @product_router.delete(
        "/{pid}",
        response_description="Product successfully deleted.",
        response_model=Response,
        responses=default_exception_list
    )
    async def delete_product(self, pid: str, current_user: User = Depends(get_current_user)):
        """
        Deletes a product.
        """
        products_service = ProductService()
        if not has_elevated_privileges(current_user):
            await products_service.validate_exists(additional_filters={"organizationPid": current_user.organizationPid})
        await products_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="Product deleted.")
