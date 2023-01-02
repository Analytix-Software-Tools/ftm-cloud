from fastapi import Body, APIRouter, HTTPException
from pydantic.validators import List

from crosscutting.exception import default_exception_list
from domains.product_types.services.product_type_service import ProductTypesService

from models.patchdocument import PatchDocument
from models.response import Response, ResponseWithHttpInfo
from models.product_type import ProductType

product_type_router = APIRouter()


@product_type_router.post("/", response_model=ProductType, response_description="Successfully registered product type.",
                          responses=default_exception_list)
async def add_product_type(new_product_type: ProductType = Body(...)):
    """Registers a new product type within the space.
    """
    product_types_service = ProductTypesService()
    new_product_type = await product_types_service.add_document(new_product_type)
    return new_product_type


@product_type_router.get("/", response_description="Product types retrieved", response_model=Response[ProductType],
                         responses=default_exception_list)
async def get_product_types(q: str | None = None, limit: int | None = None, offset: int | None = None,
                            sort: str | None = None, includeTotals: bool | None = None):
    """Gets all product types using the user defined parameters.
    """
    product_types_service = ProductTypesService()
    product_types = await product_types_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    headers = {}
    if includeTotals is not None:
        headers = {"X-Total-Count": str(await product_types_service.total(q))}
    return ResponseWithHttpInfo(data=product_types,
                                model=ProductType,
                                description="Product types retrieved successfully.",
                                headers=headers)


@product_type_router.get("/{pid}", response_description="Product type data retrieved", response_model=Response[ProductType],
                         responses=default_exception_list)
async def get_product_type(pid: str):
    """Retrieves a product type by ID.
    """
    product_types_service = ProductTypesService()
    product_type_exists = await product_types_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Product type retrieved.',
                    data=[product_type_exists])


@product_type_router.patch("/{pid}", response_model=Response, response_description="Successfully patched product type.",
                           responses=default_exception_list)
async def patch_product_type(pid: str, patch_list: List[PatchDocument] = Body(...)):
    """Patches a product type within the space.
    """
    product_types_service = ProductTypesService()
    await product_types_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Product type patched successfully.")


@product_type_router.delete("/{pid}", response_description="Product type successfully deleted.", response_model=Response,
                            responses=default_exception_list)
async def delete_product_type(pid: str):
    """Deletes a product type.
    """
    product_types_service = ProductTypesService()
    await product_types_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Product type deleted.")
