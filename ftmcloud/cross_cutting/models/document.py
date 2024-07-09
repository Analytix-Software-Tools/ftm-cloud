import datetime

from beanie import Document
from pydantic.class_validators import Optional
from pydantic.config import Extra
from pydantic.fields import Field
from pydantic.types import SecretBytes
from beanie.odm.fields import PydanticObjectId


class BaseDocument(Document):

    # id: PydanticObjectId = Field(..., exclude=True)
    createdAt: datetime.datetime = Field(default=datetime.datetime.now())
    isDeleted: SecretBytes = Field(default=False, exclude=True)

    class Config:
        extra = Extra.forbid
