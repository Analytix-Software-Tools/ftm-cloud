import datetime
from typing import Literal, List

from ftmcloud.cross_cutting.models.document import BaseDocument


class Task(BaseDocument):
    """
    Represents the status of a task within the background task system.
    """
    id: int
    status: str
    taskType: Literal['BulkProductUpload', 'BulkProductUpdate', 'ProductCategoryMigration']
    errorList: List[dict] | None
    startDatetime: datetime.datetime
    completedDatetime: datetime.datetime

