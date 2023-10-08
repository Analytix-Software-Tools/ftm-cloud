from typing import Literal

from pydantic.class_validators import Optional

from ftmcloud.models.document import BaseDocument


class ModelConfiguration(BaseDocument):
    """
    Configurations for ML processing.
    """
    pid: Optional[str]
    documentPid: str
    targetCollection: Literal["organizations", "attributes", "categories", "product_types"]
    confidenceType: Literal["strict", "loose", "moderate"] = "moderate"
    positiveKeywords: list[str]
    negativeKeywords: list[str]

    class Settings:
        name = "model_configurations"

    class Config:
        schema_extra = {
            "example": {
                "targetCollection": "categories",
                "documentPid": "Test pid",
                "pid": "Test pid",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
