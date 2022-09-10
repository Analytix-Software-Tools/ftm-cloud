from beanie import Document
from pydantic.class_validators import Optional


class Privilege(Document):
    """Represents different access control levels a user might have within
    the database.
    """
    pid: str
    name: str
    description: Optional[str]
    routes: list

    class Collection:
        name = "privileges"

    class Config:
        schema_extra = {
            "example": {
                "name": "Privilege",
                "description": "User privilege",
                "routes": [],
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
