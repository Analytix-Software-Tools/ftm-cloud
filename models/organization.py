from pydantic.class_validators import Optional

from models.document import BaseDocument


class Organization(BaseDocument):
    pid: Optional[str]
    name: str
    description: str
    imgUrl: str = ""
    addressStreet: str = ""
    addressCity: str = ""
    addressState: str = ""
    addressZip: str | int = ""
    phone: str = ""

    class Collection:
        name = "organizations"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Organization",
                "description": "Organization",
                "pid": "Test pid",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
