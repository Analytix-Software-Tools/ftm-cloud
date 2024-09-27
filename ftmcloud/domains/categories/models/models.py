from pydantic.class_validators import Optional

from ftmcloud.cross_cutting.models.document import BaseDocument


class Category(BaseDocument):
    """Represents a type of product category to standardize formatting.
    """
    pid: Optional[str]
    name: str
    description: str
    parentCategoryPid: str | None = None

    class Settings:
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
