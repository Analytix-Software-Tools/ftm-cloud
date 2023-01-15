from pydantic.class_validators import Optional

from models.attribute import AttributeValue
from models.document import BaseDocument


class Product(BaseDocument):
    """Represents a type of service to standardize formatting.
    """
    pid: Optional[str]
    name: str
    description: str
    productTypePid: str
    organizationPid: str
    attributeValues: list[AttributeValue] = []

    class Collection:
        name = "products"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Product",
                "description": "Product",
                "pid": "Test pid",
                "productTypePid": "productTypePid",
                "organizationPid": "organizationPid",
                "attributeValues": [],
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
