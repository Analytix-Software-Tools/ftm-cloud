from pydantic import BaseModel
from pydantic.schema import Literal, Any


class PatchDocument(BaseModel):
    """A document representing a transaction within a PATCH operation
    in accordance with the IETF proposed RFC-6902 JSON-Patch.

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
