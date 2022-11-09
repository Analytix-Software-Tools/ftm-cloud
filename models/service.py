from pydantic.class_validators import Optional

from models.attribute import AttributeValue
from models.document import BaseDocument


class Service(BaseDocument):
    """Represents a type of service to standardize formatting.
    """
    pid: Optional[str]
    name: str
    description: str
    serviceClassificationPid: str | None = None
    attributeValues: list[AttributeValue] = []

    class Collection:
        name = "services"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Service",
                "description": "Service",
                "pid": "Test pid",
                "serviceClassificationPid": "serviceClassificationPid",
                "attributeValues": [],
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
