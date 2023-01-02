from pydantic.class_validators import Optional

from models.document import BaseDocument


class Category(BaseDocument):
    """Represents a type of product category to standardize formatting.
    """
    pid: Optional[str]
    name: str
    description: str
    parentCategoryPid: str | None = None

    class Collection:
        name = "categories"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Category",
                "description": "Category",
                "pid": "Test pid",
                "parentCategoryPid": "parentServiceGroup",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
