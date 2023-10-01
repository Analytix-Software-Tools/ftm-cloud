from ftmcloud.core.config.config import Settings

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
        pass
