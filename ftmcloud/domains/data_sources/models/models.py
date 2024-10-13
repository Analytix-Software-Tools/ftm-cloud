from pydantic.class_validators import Optional

from ftmcloud.cross_cutting.models.document import BaseDocument
from ftmcloud.cross_cutting.repository.repository import Repository


class DataSource(BaseDocument):
    """
    Represents a unique source of data.
    """
    pid: Optional[str]
    name: str
    description: str

    class Settings:
        name = "data_sources"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Data Source",
                "description": "Data Source",
                "pid": "Test pid",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }


class DataSourceRepository(Repository):

    def __init__(self):
        super().__init__(model_cls=DataSource)
