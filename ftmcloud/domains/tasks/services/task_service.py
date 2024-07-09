from ftmcloud.cross_cutting.service.service import Service
from ftmcloud.domains.tasks.models.models import Task


class TasksService(Service):

    def __init__(self):
        """
        Initialize the TasksService.
        """
        super().__init__(collection=Task)
