import datetime
from pydantic.schema import Literal, Optional
from pydantic.main import BaseModel

from ftmcloud.cross_cutting.models.document import BaseDocument


class KeyValueRecord(BaseModel):
    """
    Represents a key value pair.
    """
    name: str
    value: str


class DataExample(BaseModel):
    """
    Represents a tangible set of example records to be used as
    context.
    """
    fieldNames: list[str]
    exampleRecords: list[dict]


class FtmTask(BaseDocument):
    """
    Represents a task to be completed for data import.
    """
    targetApplication: str
    taskDescription: str
    taskType: Literal["DatasetReview"]
    taskMetadata: list[KeyValueRecord]
    dataExample: DataExample
    assigneeUserPid: Optional[str]
    completedDatetime: Optional[datetime.datetime]
    completedResponse: Optional[str]
    privilegePids: list[str]
    lockDatetime: Optional[datetime.datetime]
    pid: Optional[str]

    class Settings:
        name = "ftm_tasks"

    class Config:
        schema_extra = {
            "example": {
            "targetApplication": "testapp",
            "taskDescription": "Test task description",
            "pid": "Test pid",
            "taskType": "datasetReview",
            "taskMetadata": [
                {
                    "name": "test",
                    "value": "test"
                }
            ],
            "dataExample": {
                "fieldNames": ["name"],
                "exampleRecords": [
                    {
                        "name": "test"
                    }
                ]
            },
            "assigneeUserPid": "",
            "completedDatetime": "2022-03-17T00:54:43.924+00:00",
            "completedResponse": "",
            "privilegePids": [],
            "createdAt": "2022-03-17T00:54:43.924+00:00"
        }
        }
