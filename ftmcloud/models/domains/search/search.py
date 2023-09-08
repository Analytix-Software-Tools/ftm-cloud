import datetime

from pydantic import BaseModel
from pydantic.class_validators import Optional


class SearchHitSource(BaseModel):
    """
    A representation of the possible source of a SearchHit.
    """
    pid: str
    name: str
    description: Optional[str]
    datetime: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "name": "name",
                "description": "description",
                "pid": "pid",
                "source": "products",
                "datetime": "2022-03-17T00:54:43.924+00:00"
            }
        }


class SearchHit(BaseModel):
    """
    A representation of a document that may be returned from a search to
    the index.
    """
    _source: SearchHitSource
    _score: float

    class Config:
        schema_extra = {
            "example": {
                "_source": {
                    "name": "name",
                    "description": "description",
                    "pid": "pid",
                    "source": "products",
                    "datetime": "2022-03-17T00:54:43.924+00:00"
                },
                "_score": 0.7231
            }
        }
