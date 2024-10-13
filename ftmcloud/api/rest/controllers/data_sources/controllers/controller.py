from fastapi import Body, APIRouter
from pydantic.validators import List

from ftmcloud.core.exception.exception import default_exception_list, FtmException

from ftmcloud.cross_cutting.models.patchdocument import PatchDocument
from ftmcloud.cross_cutting.models.response import Response, ResponseWithHttpInfo
from ftmcloud.domains.data_sources.models.models import DataSource
from ftmcloud.domains.data_sources.services.data_source_services import DataSourcesService
from ftmcloud.cross_cutting.views.views import controller

router = APIRouter()


@controller(router)
class DataSourcesController:

    @router.post("/", response_model=DataSource, response_description="Successfully registered data_source.",
                 responses=default_exception_list)
    async def add_data_source(self, new_data_source: DataSource = Body(...)):
        """Registers a new data_source within the space.
        """
        data_source_service = DataSourcesService()
        data_source_exists = await data_source_service.find_one({"name": new_data_source.name})
        if data_source_exists:
            raise FtmException('error.data_source.InvalidName')
        await data_source_service.add_document(new_data_source)
        return new_data_source

    @router.get("/", response_description="DataSources retrieved", response_model=Response[DataSource],
                responses=default_exception_list)
    async def get_data_sources(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None, includeTotals: bool | None = None):
        """Gets all data_sources using the user defined parameters.
        """
        data_source_service = DataSourcesService()
        data_sources = await data_source_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await data_source_service.total(q))}
        return ResponseWithHttpInfo(data=data_sources,
                                    model=DataSource,
                                    description="DataSources retrieved successfully.",
                                    headers=headers)

    @router.get("/{pid}", response_description="DataSource data retrieved", response_model=Response[DataSource],
                responses=default_exception_list)
    async def get_data_source(self, pid: str):
        """Retrieves an data_source by ID.
        """
        data_source_service = DataSourcesService()
        data_source = await data_source_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='DataSource retrieved.',
                        data=[data_source])

    @router.patch("/{pid}", response_model=Response, response_description="Successfully patched data_source.",
                  responses=default_exception_list)
    async def patch_data_source(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches an data_source within the space.
        """
        industy_service = DataSourcesService()
        await industy_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="DataSource patched successfully.")

    @router.delete("/{pid}", response_description="DataSource successfully deleted.", response_model=Response,
                   responses=default_exception_list)
    async def delete_data_source(self, pid: str):
        """Deletes a user.
        """
        data_source_service = DataSourcesService()
        await data_source_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="DataSource deleted.")
