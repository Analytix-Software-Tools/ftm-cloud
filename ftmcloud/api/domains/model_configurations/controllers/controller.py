from fastapi import Body, APIRouter, Depends
from pydantic.validators import List
from ftmcloud.core.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list, FtmException

from ftmcloud.api.domains.users.services.user_services import UserService
from ftmcloud.models.patchdocument import PatchDocument
from ftmcloud.models.response import Response, ResponseWithHttpInfo
from ftmcloud.models.domains.model_configurations.model_configuration import ModelConfiguration
from ftmcloud.models.domains.users.user import User
from ftmcloud.api.domains.model_configurations.services.model_configuration_services import ModelConfigurationsService
from ftmcloud.utils.views import controller

router = APIRouter()


@controller(router)
class ModelConfigurationsController:
    current_user: User = Depends(get_current_user)

    @router.post(
        "/",
        response_model=ModelConfiguration,
        response_description="Successfully registered model_configuration.",
        responses=default_exception_list
    )
    async def add_model_configuration(self, new_model_configuration: ModelConfiguration = Body(...)):
        """Registers a new model_configuration within the space.
        """
        model_configuration_services = ModelConfigurationsService()
        model_configuration_exists = await model_configuration_services.find_one(
            {"targetCollection": new_model_configuration.targetCollection, "documentPid": new_model_configuration.documentPid}
        )
        if model_configuration_exists:
            raise FtmException('error.model_configuration.ModelConfigurationExists')
        await model_configuration_services.add_document(new_model_configuration)
        return new_model_configuration

    @router.get(
        "/",
        response_description="ModelConfigurations retrieved",
        response_model=Response[ModelConfiguration],
        responses=default_exception_list
    )
    async def get_model_configurations(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                                sort: str | None = None, includeTotals: bool | None = None):
        """Gets all model_configurations using the user defined parameters.
        """
        model_configuration_service = ModelConfigurationsService()
        model_configurations = await model_configuration_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await model_configuration_service.total(q))}
        return ResponseWithHttpInfo(data=model_configurations,
                                    model=ModelConfiguration,
                                    description="ModelConfigurations retrieved successfully.",
                                    headers=headers)

    @router.get(
        "/{pid}",
        response_description="ModelConfiguration data retrieved",
        response_model=Response[ModelConfiguration],
        responses=default_exception_list
    )
    async def get_model_configuration(self, pid: str):
        """Retrieves an model_configuration by ID.
        """
        model_configuration_service = ModelConfigurationsService()
        model_configuration = await model_configuration_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='ModelConfiguration retrieved.',
                        data=[model_configuration])

    @router.patch(
        "/{pid}",
        response_model=Response,
        response_description="Successfully patched model_configuration.",
        responses=default_exception_list
    )
    async def patch_model_configuration(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches an model_configuration within the space.
        """
        model_configuration_service = ModelConfigurationsService()
        await model_configuration_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="ModelConfiguration patched successfully.")

    @router.delete(
        "/{pid}",
        response_description="ModelConfiguration successfully deleted.",
        response_model=Response,
        responses=default_exception_list
    )
    async def delete_model_configuration(self, pid: str):
        """Deletes a user.
        """
        model_configuration_service = ModelConfigurationsService()
        await model_configuration_service.delete_document(pid=pid)
        return Response(status_code=200, response_type="success", description="ModelConfiguration deleted.")
