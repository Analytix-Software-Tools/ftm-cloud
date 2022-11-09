from pydantic.class_validators import Optional

from models.document import BaseDocument


class ServiceClassification(BaseDocument):
    """Represents a type of service to standardize formatting.
    """
    pid: Optional[str]
    name: str
    description: str
    parentServiceClassificationPid: str | None = None

    class Collection:
        name = "service_classifications"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Service",
                "description": "Service",
                "pid": "Test pid",
                "parentServiceClassificationPid": "parentServiceGroup",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
