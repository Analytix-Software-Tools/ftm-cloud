from pydantic.validators import List

from fastapi import APIRouter, Body
from domains.reports.services.report_service import ReportService
from crosscutting.exception import default_exception_list
from models.attribute import AttributeValue
from models.product import Product
from models.reports import HitList, ProductSearchQuery

from models.response import Response

router = APIRouter()


@router.post('/products', response_description="Successfully retrieved hits.", response_model=Response[HitList[Product]],
                    responses=default_exception_list)
async def search_products(query: ProductSearchQuery = Body(...)):
    reports_service = ReportService()
    hit_list = await reports_service.search_products(searchText=query.searchText, productTypePid=query.productTypePid,
                                                     limit=query.limit, requirements=query.requirements)
    return Response(status_code=200, description="Success", response_type="success", data=[hit_list])
