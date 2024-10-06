import json
from datetime import datetime, timedelta

from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.ftm_tasks.models.models import FtmTask


class FtmTasksService(Service):

    def __init__(self):
        super(FtmTasksService, self).__init__(collection=FtmTask)

    async def get_task_assignment(
            self,
            user_pid: str,
            offset: int = 0,
            taskType: str | None = None,
            taskStatus: str | None = None,
            targetApplication: str | None = None,
            showCompleted: bool | None = None,
    ) -> FtmTask:
        """ Assigns a task to a given user so that other users cannot simultaneously access and ensures
        any other tasks aren't being modified.

        :param user_pid: str
            pid of the user accessing the task
        :param offset: int
            offset from the first doc
        :param taskType: str | None
            the task type filter
        :param taskStatus: str | None
            the task status filter
        :param targetApplication: str | None
            the target application filter
        :param showCompleted: bool | None
            whether to show completed

        :return: ftm_task: FtmTask
            the assigned task
        """

        # Retrieve any tasks expired or missing a lockdatetime to get the 'available' tasks.
        query = {
            "$or": [
                {"lockDatetime": {"$lt": datetime.now() - timedelta(minutes=15)}},
                {"lockDatetime": None}
            ],
            "completedDatetime": None if not showCompleted else {"$ne": None}
        }
        for k, v in {
            "taskType": taskType,
            "taskStatus": taskStatus,
            "targetApplication": targetApplication
        }.items():
            if v is not None:
                query[k] = v
        available_task = await self.collection.find_one(
            query,
            skip=offset,
            sort=[("createdAt", -1)]
        )

        # Unlock any existing task completed by the user.
        await self.collection.find(
            {"assigneeUserPid": user_pid}
        ).update({"$unset": {"assigneeUserPid": "", "lockDatetime": ""}})

        return available_task

