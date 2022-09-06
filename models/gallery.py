from pydantic.class_validators import Optional

from models.document import BaseDocument


class Gallery(BaseDocument):
    pid: Optional[str]
    name: str
    description: str = ""
    imgUrl: str = ""
    userPids: list
    organizationPid: str

    class Collection:
        name = "galleries"

    class Config:
        schema_extra = {
            "example": {
                "pid": "6245c82b1b91870b51573438",
                "name": "Test gallery",
                "userPids": ["6245c82b1b91870b51573438", "6245c82b1b91870b51573439"],
                "createdByPid": "6245c82b1b91870b51573438",
                "isDeleted": "false",
                "organizationPid": "6245c82b1b91870b51573438",
                "pid": "userPid",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
        underscore_attrs_are_private = True
