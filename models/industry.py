from pydantic.class_validators import Optional

from models.document import BaseDocument


class Industry(BaseDocument):
    """Represents a grouping of organizations that exist within the space.
    """
    pid: Optional[str]
    name: str
    description: str

    class Collection:
        name = "industries"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Organization",
                "description": "Organization",
                "pid": "Test pid",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
