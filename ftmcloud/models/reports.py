from pydantic import BaseModel
from pydantic.generics import GenericModel
from pydantic.schema import Generic
from pydantic.typing import Dict

from ftmcloud.models.attribute import AttributeValue
from ftmcloud.models.response import DataT


class ProductSearchQuery(BaseModel):
    """
    Represents a request model that allows the user to specify a query.
    """
    searchText: str
    productTypePid: str
    requirements: list[AttributeValue]
    limit: int = 10
    offset: int = 0

    class Config:
        scheme_extra = {
            "example": {
                "searchText": "Search Text",
                "productTypePid": "productTypePid",
                "limit": 10,
                "offset": 0,
                "requirements": [
                    {
                        "attributePid": "attributePid",
                        "value": {
                            "numValue": 4
                        }
                    }
                ]
            }
        }


class Hit(GenericModel, Generic[DataT]):
    """Represents a ranked result as designated in a HitList. Scoring varies
    based on the search algorithm that is applied.
    """

    hit: DataT
    score: float

    class Config:
        schema_extra = {
            "example": {
                "hit": {
                    "name": "Product Name",
                    "description": "Product Description",
                    "organizationPid": "Organization Pid",
                    "attributeValues": [],
                },
                "score": -1.1
            }
        }


class HitList(GenericModel, Generic[DataT]):
    """Hitlists are the results of search endpoints. Generally, results in the hitlist
    are ranked based on relevance.
    """
    hits: list[Hit[DataT]] = []
    total: int = 0
    maxScore: float = 0.0

    class Config:
        schema_extra = {
            "example": {
                "hits": [
                    {
                        "hit": {
                            "name": "Product Name",
                            "description": "Product Description",
                            "organizationPid": "Organization Pid",
                            "attributeValues": [],
                        },
                        "score": -1.1
                    }
                ],
                "total": 1,
                "maxScore": -1.1
            }
        }
