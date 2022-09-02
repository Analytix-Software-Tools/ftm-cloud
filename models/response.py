from typing import Generic, TypeVar, Optional, List

from pydantic.generics import GenericModel

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