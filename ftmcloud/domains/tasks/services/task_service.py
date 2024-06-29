from ftmcloud.common.service.service import Service
from ftmcloud.models.domains.task import Task


class TasksService(Service):

    def __init__(self):
        """
        Initialize the TasksService.
        """
        super().__init__(collection=Task)
