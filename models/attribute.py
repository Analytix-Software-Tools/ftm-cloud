import pydantic
from pydantic.class_validators import Optional, root_validator
from pydantic import BaseModel
from pydantic.schema import Literal, Any

from models.document import BaseDocument


class Attribute(BaseDocument):
    """Represents an attribute that can exist on a service.
    """
    pid: Optional[str]
    name: str
    description: str
    type: Literal["number", "range", "text", "dropdown"]

    class Collection:
        name = "attributes"

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Attribute",
                "description": "Attribute",
                "pid": "Test pid",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }


class AttributeNumberValue(BaseModel):
    numValue: int

    class Config:
        scheme_extra = {
            "example": {
                "numValue": 4
            }
        }


class AttributeBooleanValue(BaseModel):
    value: bool

    class Config:
        scheme_extra = {
            "example": {
                "value": "true"
            }
        }


class AttributeTextValue(BaseModel):
    value: str

    class Config:
        scheme_extra = {
            "example": {
                "value": "value"
            }
        }


class AttributeRangeValue(BaseModel):
    minValue: int
    maxValue: int

    class Config:
        scheme_extra = {
            "example": {
                "minValue": 4,
                "maxValue": 20
            }
        }

    @root_validator(pre=True)
    def validate_min_max_values(cls, values):
        min_value, max_value = values.get('minValue'), values.get('maxValue')
        if min_value is not None and max_value is not None:
            if min_value >= max_value:
                raise ValueError("Value for field 'minValue' cannot exceed 'maxValue'")
        return values


class AttributeDropdownValue(BaseModel):
    options: list[str]
    value: str | None

    class Config:
        scheme_extra = {
            "example": {
                "options": ["test value", "test value 2"],
                "value": "test value"
            }
        }

    @root_validator(pre=True)
    def validate_value_in_options(cls, values):
        options, value = values.get('options'), values.get('value')
        if options is not None and value is not None:
            if value not in options:
                raise ValueError(f"Bad value '{value}' not found in attributeValues.value.options")
        return values


class AttributeValue(BaseModel):
    """Attribute values are mappings of respective attribute PIDs to
    any arbitrary value that can exist.

    """
    attributePid: str
    value: AttributeNumberValue | AttributeDropdownValue | AttributeRangeValue | AttributeTextValue | AttributeBooleanValue
    isRequired: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "attributePid": "Attribute Pid",
                "value": {"value": 4},
                "isRequired": "true"
            }
        }
