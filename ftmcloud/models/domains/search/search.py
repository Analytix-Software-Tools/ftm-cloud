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
                    "_timestamp": "2023-11-03T23:10:58.208839+00:00",
                    "id": "id"
            }
        }


class SearchHit(BaseModel):
    """
    A representation of a document that may be returned from a search to
    the index.
    """
    _source: SearchHitSource
    _score: float
    _index: str
    _id: str

    class Config:
        schema_extra = {
            "example": {
                "_source": {
                    "name": "name",
                    "description": "description",
                    "pid": "pid",
                    "source": "products",
                    "_timestamp": "2023-11-03T23:10:58.208839+00:00",
                    "id": "id"
                },
                "_score": 0.7231,
                "_index": "_index",
                "_id": "_id"
            }
        }
