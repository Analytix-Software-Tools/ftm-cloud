from fastapi import Body, APIRouter, Depends
from pydantic.schema import Optional, Literal
from pydantic.validators import List

from ftmcloud.core.exception.exception import default_exception_list, FtmException
from ftmcloud.cross_cutting.auth.jwt_bearer import get_current_user
from ftmcloud.domains.ftm_tasks.services.ftm_task_services import FtmTasksService
from ftmcloud.domains.product_types.services.product_type_service import ProductTypesService

from ftmcloud.cross_cutting.models.patchdocument import PatchDocument
from ftmcloud.cross_cutting.models.response import Response, ResponseWithHttpInfo
from ftmcloud.domains.ftm_tasks.models.models import FtmTask
from ftmcloud.cross_cutting.views.views import controller
from ftmcloud.domains.users.models.models import User

ftm_tasks_router = APIRouter()


@controller(ftm_tasks_router)
class FtmTasksController:

    @ftm_tasks_router.post("/", response_model=FtmTask, response_description="Successfully registered ftm_task.",
                           responses=default_exception_list)
    async def add_ftm_task(self, new_ftm_task: FtmTask = Body(...)):
        """Registers a new ftm_task within the space.
        """
        ftm_tasks_service = FtmTasksService()
        new_ftm_task = await ftm_tasks_service.add_document(new_ftm_task)
        return new_ftm_task

    @ftm_tasks_router.get("/", response_description="FtmTasks retrieved", response_model=Response[FtmTask],
                          responses=default_exception_list)
    async def get_ftm_tasks(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                            sort: str | None = None, includeTotals: bool | None = None):
        """Gets all ftm_tasks using the user defined parameters.
        """
        ftm_tasks_service = FtmTasksService()
        ftm_tasks = await ftm_tasks_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await ftm_tasks_service.total(q))}
        return ResponseWithHttpInfo(data=ftm_tasks,
                                    model=FtmTask,
                                    description="FtmTasks retrieved successfully.",
                                    headers=headers)

    @ftm_tasks_router.patch(
        "/{pid}",
        response_model=Response,
        response_description="Successfully patched FtmTask.",
        responses=default_exception_list)
    async def patch_ftm_task(self, pid: str, patch_list: List[PatchDocument] = Body(...),
                            current_user: User = Depends(get_current_user)):
        """
        Patches a product within the space.
        """
        ftm_tasks_service = FtmTasksService()
        await ftm_tasks_service.validate_exists(
            pid=pid,
            additional_filters={}
        )
        await ftm_tasks_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="FtmTask patched successfully.")

    @ftm_tasks_router.get(
        "/assign",
        response_description="Successfully got a task assignment.",
        response_model=Response[FtmTask],
        responses=default_exception_list
    )
    async def get_task_assignment(
            self,
            offset: int | None = None,
            taskType: str | None = None,
            taskStatus: Literal["completed"] | None = None,
            targetApplication: Literal["moodme", "analytix"] | None = None,
            current_user: User = Depends(get_current_user)
    ) -> FtmTask:
        """ Retrieves a task assignment based on the current user and their organization's
        assigned task types. Assigns a single task to the user, hiding the rest from other
        users.

        :param taskType: str
            the type of task
        :param taskStatus: str
            status of the task
        :param targetApplication: "moodme" or "analytix"
            the target application filter

        :return: assigned_task: FtmTask
            the assigned task
        """
        ftm_tasks_service = FtmTasksService()

        assigned_task = await ftm_tasks_service.get_task_assignment(
            user_pid=current_user.pid
        )

        if assigned_task is None:
            data = []
        else:
            data = [assigned_task]

        headers = {"X-Total-Count": str(await ftm_tasks_service.total('{}'))}

        return ResponseWithHttpInfo(
            data=data,
            model=FtmTask,
            description="Task assignment retrieved successfully.",
            headers=headers
        )

    @ftm_tasks_router.get("/{pid}", response_description="FtmTask data retrieved", response_model=Response[FtmTask],
                          responses=default_exception_list)
    async def get_ftm_task(self, pid: str):
        """Retrieves a ftm_task by ID.
        """
        ftm_tasks_service = FtmTasksService()
        ftm_task_exists = await ftm_tasks_service.validate_exists(pid=pid)
        return Response(status_code=200, response_type='success', description='FtmTask retrieved.',
                        data=[ftm_task_exists])

    @ftm_tasks_router.patch("/{pid}", response_model=Response, response_description="Successfully patched ftm_task.",
                            responses=default_exception_list)
    async def patch_ftm_task(self, pid: str, patch_list: List[PatchDocument] = Body(...)):
        """Patches a ftm_task within the space.
        """
        ftm_tasks_service = FtmTasksService()
        await ftm_tasks_service.patch(pid=pid, patch_document_list=patch_list)
        return Response(status_code=204, response_type='success', description="FtmTask patched successfully.")
