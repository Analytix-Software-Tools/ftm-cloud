from pydantic.class_validators import Optional

from models.attribute import AttributeValue
from models.document import BaseDocument


class ProductType(BaseDocument):
    """Represents a type of service to standardize formatting.
    """
    pid: Optional[str]
    name: str
    description: str
    categoryPid: str | None = None
    attributeValues: list[AttributeValue] = []

    class Collection:
        name = "product_types"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Product Type",
                "description": "Product Type",
                "pid": "Test pid",
                "categoryPid": "categoryPid",
                "attributeValues": [],
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
