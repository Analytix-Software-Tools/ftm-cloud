from pydantic import BaseModel


class HttpError(BaseModel):
    """An exception model that contains messages to be displayed on the
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
                "errorCode": "exception.demo.ExampleError",
                "developerMessage": "Try a different exception.",
                "userMessage": "userMessage",
                "statusCode": 500,
                "info": "http://www.example.com/exampleError.html"
            }
        }
