from fastapi import APIRouter, Depends

from ftmcloud.api.domains.tasks.services.task_service import TasksService
from ftmcloud.common.auth.jwt_bearer import get_current_user
from ftmcloud.core.exception.exception import default_exception_list

from ftmcloud.models.response import Response
from ftmcloud.models.domains.task import TaskResponse
from ftmcloud.models.domains.user import User
from ftmcloud.common.views.views import controller

router = APIRouter()


@controller(router)
class TasksController:

    @router.get(
        "/{task_id}",
        response_description="Task data retrieved",
        response_model=Response[TaskResponse],
        responses=default_exception_list
    )
    async def get_task(self, task_id: int, current_user: User = Depends(get_current_user)):
        """
        Retrieves a task from the task queue by ID.
        """
        tasks_service = TasksService()
        tasks_service.get_task(task_id=task_id)
        return Response(status_code=200, response_type='success', description='Task status retrieved.',
                        data=[])
