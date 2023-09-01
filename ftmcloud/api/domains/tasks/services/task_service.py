from ftmcloud.core.exception.exception import FtmException
from ftmcloud.core.service import AbstractService


class TasksService(AbstractService):

    def __init__(self):
        """
        Initialize the TasksService.
        """
        super().__init__()

    def get_task(
            self, task_id
    ):
        """
        Retrieves the task by ID from the task backend.

        :param task_id: the id of the task
        :return: the task stored in the backend
        """
        raise Exception("Not implemented yet.")
