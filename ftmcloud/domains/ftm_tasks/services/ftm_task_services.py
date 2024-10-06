import json
from datetime import datetime, timedelta

from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.cross_cutting.session.session import validate_user_privilege_in_list
from ftmcloud.domains.ftm_tasks.models.models import FtmTask
from ftmcloud.domains.users.models.models import User


class FtmTasksService(Service):

    def __init__(self):
        super(FtmTasksService, self).__init__(collection=FtmTask)

    def _date_to_iso_string(self, dt):
        return dt.isoformat() + 'Z'

    async def patch_document_validator(self, document, patch_document_list, current_user: User | None = None):
        """ Validates FtmTask patch documents.

        :param document:
        :param patch_document_list:
        :param current_user: User | None
        :return:
        """
        for _patch_doc in patch_document_list:
            match _patch_doc['path']:
                case 'completedResponse':
                    document['assigneeUserPid'] = current_user.pid
                    document['completedDatetime'] = datetime.now()
                case _:
                    # Don't allow the user to change any metadata about the task.
                    if validate_user_privilege_in_list(current_user.privilegePid, ['reviewer', 'user']):
                        raise FtmException('error.patch.invalidPatch')

    def get_task_assignment_query(
            self,
            taskType: str | None = None,
            taskStatus: str | None = None,
            targetApplication: str | None = None,
            showCompleted: bool | None = None,
    ):
        """ Gets a query to fetch assignable tasks.

        :param taskType: str | None
            the task type filter
        :param taskStatus: str | None
            the task status filter
        :param targetApplication: str | None
            the target application filter
        :param showCompleted: bool | None
            whether to show completed

        :return: query: dict
            the query
        """
        assignable_q = {
            "$or": [
                {"lockDatetime": {"$lt": self._date_to_iso_string(datetime.now() - timedelta(minutes=15))}},
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
                assignable_q[k] = v
        return assignable_q

    async def get_task_assignment(
            self,
            user_pid: str,
            offset: int = 0,
            query: dict | None = None,
    ) -> FtmTask:
        """ Assigns a task to a given user so that other users cannot simultaneously access and ensures
        any other tasks aren't being modified.

        :param user_pid: str
            pid of the user accessing the task
        :param offset: int
            offset from the first doc
        :param query: dict | None
            the query to use

        :return: ftm_task: FtmTask
            the assigned task
        """

        # Retrieve any tasks expired or missing a lockdatetime to get the 'available' tasks.

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

