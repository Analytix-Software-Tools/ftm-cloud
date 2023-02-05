from fastapi import APIRouter, Body
from starlette.requests import Request

from config.config import limiter
from domains.reports.services.report_service import ReportService
from crosscutting.error.exception import default_exception_list
from models.product import Product
from models.reports import HitList, ProductSearchQuery

from models.response import Response

router = APIRouter()


@router.post('/products', response_description="Successfully retrieved hits.",
             response_model=Response[HitList[Product]],
             responses=default_exception_list)
@limiter.limit('30/minute')
async def search_products(request: Request, query: ProductSearchQuery = Body(...)):
    """

    Retrieves products that accurately fit a user-specified requirement.

    :param request: the user request, passed into the rate-limiter
    :param query: represents the current query
    :return: a list of hits, organized by score
    """
    reports_service = ReportService()
    hit_list = await reports_service.search_products(searchText=query.searchText, productTypePid=query.productTypePid,
                                                     limit=query.limit, requirements=query.requirements)
    return Response(status_code=200, description="Success", response_type="success", data=[hit_list])
