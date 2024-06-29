from fastapi import APIRouter, Depends

from ftmcloud.domains.search.services.search_service import SearchService
from ftmcloud.common.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list

from ftmcloud.models.response import ResponseWithHttpInfo, Response
from ftmcloud.models.domains.search import SearchHit
from ftmcloud.models.domains.user import User
from ftmcloud.common.views.views import controller

router = APIRouter()


@controller(router)
class SearchController:

    @router.get(
        "/",
        response_description="Search results retrieved.",
        response_model=Response[SearchHit],
        responses=default_exception_list
    )
    async def search(
            self,
            q: str,
            fields: list[dict]=None,
            limit: int=10,
            offset: int=0,
            includeTotals: bool=False,
            current_user: User = Depends(get_current_user)
    ):
        """
        Retrieves a task from the task queue by ID.
        """
        search_service = SearchService()
        results, total = await search_service.search(
            q=q,
            fields=fields,
            limit=limit,
            offset=offset,
            include_totals=includeTotals,
            additional_filters=None
        )
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(total)}
        return ResponseWithHttpInfo(status_code=200, response_type='success', description='Search hits retrieved.',
                                    data=results["hits"]["hits"], model=SearchHit, headers=headers)
