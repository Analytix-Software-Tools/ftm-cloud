from pydantic.class_validators import Optional

from models.document import BaseDocument


class Industry(BaseDocument):
    """Represents a grouping of organizations that exist within the space.
    """
    pid: Optional[str]
    name: str
    description: str
    naicsCode: int | None = None

    class Collection:
        name = "industries"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Industry",
                "description": "Industry",
                "pid": "Test pid",
                "naicsCode": 12345,
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
