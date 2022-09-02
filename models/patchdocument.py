from pydantic import BaseModel
from pydantic.schema import Literal, Any


class PatchDocument(BaseModel):
    """This model is used to enforce consistency with a user's patch
    document.

    """
    op: Literal["add", "remove", "replace", "copy", "move", "test"]
    path: str
    value: Any

    class Config:
        schema_extra = {
            "example": {
                "op": "add",
                "path": "/name",
                "value": "New name value",
            }
        }
