from typing import Generic, TypeVar, Optional, List

from pydantic.generics import GenericModel
from pydantic.main import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from models.user import User

DataT = TypeVar('DataT')


class Response(GenericModel, Generic[DataT]):
    """This is a generic model that is used to enforce consistency
    within an endpoint response. The data-type is asserted with the Generic
    parameter which will ensure that any data provided within the data array
    conforms to specification.

    """
    status_code: int
    response_type: str
    description: str
    data: Optional[List[DataT]]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }


class LoginResponse(BaseModel):
    accessToken: str
    user: User

    class Config:
        schema_extra = {
            "example": {
                "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIwN2Y5MTVmNC1hNTBmLTRhM2UtODJkNi0yMzBmMzZhZTM3YjQiLCJwcml2aWxlZ2UiOlsiZ2FsbGVyaWVzOmdldCIsInV…",
                "user": {
                    "userFields"
                },
            }
        }


class ResponseWithHttpInfo(JSONResponse, Generic[DataT]):
    """Wraps the raw response model to allow fields such as the headers to be set. Ensures that data in the response
    model aligns with the taxonomy of the designated model.

    """

    def __init__(self, model, status_code: int = 200, response_type: str = "success",
                 data: Optional[List[DataT]] = None, description: str = "Success",
                 *args, **kwargs):
        super().__init__(
            content=jsonable_encoder(Response[model](status_code=status_code,
                                                     response_type=response_type,
                                                     description=description,
                                                     data=data)) if data is not None else None,
            media_type="application/json",
            status_code=status_code,
            *args,
            **kwargs,
        )
