from pydantic import BaseModel
from pydantic.schema import Literal, Any


class HttpError(BaseModel):
    """An error model that contains messages to be displayed on the
    frontend.
    """
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Error detail"
            }
        }
