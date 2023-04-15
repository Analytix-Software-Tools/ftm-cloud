from beanie import Indexed
from pydantic.class_validators import Optional

from ftmcloud.models.attribute import AttributeValue
from ftmcloud.models.document import BaseDocument


class Product(BaseDocument):
    """Represents a type of service to standardize formatting.
    """
    pid: Indexed(str, unique=True)
    name: str
    description: str
    imgUrl: str = ""
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
                "imgUrl": "imgUrl",
                "pid": "Test pid",
                "productTypePid": "productTypePid",
                "organizationPid": "organizationPid",
                "attributeValues": [],
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
