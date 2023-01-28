from fastapi import Body, APIRouter
from pydantic.validators import List

from crosscutting.error.exception import default_exception_list
from domains.products.services.product_service import ProductService

from models.patchdocument import PatchDocument
from models.product import Product
from models.response import Response, ResponseWithHttpInfo

product_router = APIRouter()


@product_router.post("/", response_model=Product, response_description="Successfully registered product.",
                          responses=default_exception_list)
async def add_product(new_product: Product = Body(...)):
    """Registers a new product within the space.
    """
    products_service = ProductService()
    new_product = await products_service.add_document(new_product)
    return new_product


@product_router.get("/", response_description="Products retrieved", response_model=Response[Product],
                         responses=default_exception_list)
async def get_products(q: str | None = None, limit: int | None = None, offset: int | None = None,
                            sort: str | None = None, includeTotals: bool | None = None):
    """Gets all products using the user defined parameters.
    """
    products_service = ProductService()
    products = await products_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    headers = {}
    if includeTotals is not None:
        headers = {"X-Total-Count": str(await products_service.total(q))}
    return ResponseWithHttpInfo(data=products,
                                model=Product,
                                description="Products retrieved successfully.",
                                headers=headers)


@product_router.get("/{pid}", response_description="Product data retrieved", response_model=Response[Product],
                         responses=default_exception_list)
async def get_product(pid: str):
    """Retrieves a product by ID.
    """
    products_service = ProductService()
    product_exists = await products_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Product retrieved.',
                    data=[product_exists])


@product_router.patch("/{pid}", response_model=Response, response_description="Successfully patched product.",
                           responses=default_exception_list)
async def patch_product(pid: str, patch_list: List[PatchDocument] = Body(...)):
    """Patches a product within the space.
    """
    products_service = ProductService()
    await products_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Product patched successfully.")


@product_router.delete("/{pid}", response_description="Product successfully deleted.", response_model=Response,
                            responses=default_exception_list)
async def delete_product(pid: str):
    """Deletes a product.
    """
    products_service = ProductService()
    await products_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Product deleted.")
