from starlette.background import BackgroundTask

from ftmcloud.core.config.config import Settings
from uuid import uuid4

from ftmcloud.core.exception.exception import FtmException
from ftmcloud.domains.tasks.models.models import Task

settings = Settings()


class BackgroundTaskManager:

    def __init__(self):
        """
        Initialize a new BackgroundTaskManager.
        """
        self._tasks_collection = Task

    def abort_task_failed(self, pid: str):
        pass

    def init_task(self):
        pass

    def enqueue_task(self, background_tasks: BackgroundTask, name: str, body: dict):
        """ Enqueues a task.

        :param background_tasks: BackgroundTask
            The background task to execute
        :param name: str
            The name of the task to execute
        :param body: dict
            The body of the task
        :return:
        """
        try:
            new_task = Task()
            new_task.set({
                "pid": str(uuid4()),
                "": ""
            })
            self._tasks_collection.insert_one()
        except:
            raise FtmException("")

    def run_task(self):
        pass
