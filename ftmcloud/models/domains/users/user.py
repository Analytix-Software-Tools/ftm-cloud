from pydantic import BaseModel, EmailStr
from pydantic.class_validators import Optional
from pydantic.fields import Field
from pydantic.types import SecretStr

from ftmcloud.models.document import BaseDocument
from ftmcloud.models.domains.organizations.organization import Organization
from ftmcloud.models.domains.privileges.privilege import Privilege


class User(BaseDocument):
    pid: Optional[str]
    firstName: str
    lastName: str
    imgUrl: str = ""
    email: EmailStr
    organizationPid: str
    privilegePid: str = "2fe4b840-0a27-4b5f-98cd-e6080c228eec"
    addressStreet1: str = ""
    addressStreet2: str = ""
    city: str = ""
    state: str = ""
    country: str = ""
    zip: str = ""
    phone: str = ""
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "firstName": "First",
                "lastName": "Last",
                "email": "user@user.com",
                "galleryPids": ["6245c82b1b91870b51573438", "6245c82b1b91870b51573439"],
                "privilegePid": "6245c82b1b91870b51573559",
                "isDeleted": "false",
                "organizationPid": "organization",
                "pid": "userPid",
                "addressStreet1": "1 Test Avenue",
                "addressStreet2": "",
                "city": "Testville",
                "state": "VT",
                "country": "USA",
                "phone": "(856) 123-4567",
                "createdAt": "2022-03-17T00:54:43.924+00:00"
            }
        }
        underscore_attrs_are_private = True


class UserSignIn(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@user.com",
                "password": "F3e587!#xsz$$%"
            }
        }


class UserResponse(User):
    password: SecretStr = Field(..., exclude=True)

    class Config:
        schema_extra = {
            "example": {
                "firstName": "First",
                "lastName": "Last",
                "email": "user@user.com",
            }
        }


class UserProfile(UserResponse):
    organization: Organization
    privilege: Privilege

    class Config:
        schema_extra = {
            "example": {
                "pid": "pid",
                "firstName": "First",
                "lastName": "Last",
                "email": "user@user.com",
                "imgUrl": "imgUrl",
                "galleryPids": [],
                "organizationPid": "organizationPid",
                "privilegePid": "privilegePid",
                "organization": {"organization"},
                "privilege": {
                    "privilege"
                }
            }
        }
