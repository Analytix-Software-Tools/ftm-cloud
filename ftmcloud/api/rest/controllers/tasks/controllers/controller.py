from fastapi import APIRouter, Depends

from ftmcloud.domains.tasks.services.task_service import TasksService
from ftmcloud.cross_cutting.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list

from ftmcloud.cross_cutting.models.response import Response, ResponseWithHttpInfo
from ftmcloud.domains.tasks.models.models import Task
from ftmcloud.domains.users.models.models import User
from ftmcloud.cross_cutting.views.views import controller

router = APIRouter()


@controller(router)
class TasksController:

    @router.get("/", response_description="Tasks retrieved", response_model=Response[Task])
    async def get_tasks(self, q: str | None = None, limit: int | None = None, offset: int | None = None,
                             sort: str | None = None,
                             includeTotals: bool | None = None):
        """Gets all tasks using the user defined parameters.
        """
        task_service = TasksService()
        privileges = await task_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
        headers = {}
        if includeTotals is not None:
            headers = {"X-Total-Count": str(await task_service.total(q=q))}
        return ResponseWithHttpInfo(status_code=200,
                                    response_type='success',
                                    model=Task,
                                    description="Tasks retrieved successfully.",
                                    data=privileges,
                                    headers=headers)

    @router.delete(
        "/{pid}",
        response_description="Task successfully deleted.",
        response_model=Response,
        responses=default_exception_list
    )
    async def delete_task(self, pid: str, current_user: User = Depends(get_current_user)):
        """
        Deletes a task.
        """
        tasks_service = TasksService()
        await tasks_service.delete_document(pid=pid, additional_filters={"completedDatetime": {"$exists": True}})
        return Response(status_code=200, response_type="success", description="Product deleted.")
