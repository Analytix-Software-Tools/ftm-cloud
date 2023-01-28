from pydantic import BaseModel
from pydantic.schema import Literal, Any


class HttpError(BaseModel):
    """An error model that contains messages to be displayed on the
    frontend.
    """
    errorCode: str
    developerMessage: str
    userMessage: str
    statusCode: int
    info: str

    class Config:
        schema_extra = {
            "example": {
                "errorCode": "error.demo.ExampleError",
                "developerMessage": "Try a different error.",
                "userMessage": "userMessage",
                "statusCode": 500,
                "info": "http://www.example.com/exampleError.html"
            }
        }
