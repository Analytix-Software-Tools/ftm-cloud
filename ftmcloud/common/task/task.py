from ftmcloud.core.config.config import Settings
from uuid import uuid4

from ftmcloud.core.exception.exception import FtmException

settings = Settings()


class BackgroundTaskManager:

    def __init__(self):
        """
        Initialize a new BackgroundTaskManager.
        """
        pass

    def enqueue_task(self, name: str, body: dict):
        """ Enqueues a task by pushing a message onto the message broker.

        :param name: the name of the task to execute
        :param body: the body of the task
        :return:
        """
        try:
            new_task_pid = uuid4()

        except:
            raise FtmException("")
