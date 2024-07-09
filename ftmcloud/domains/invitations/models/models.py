from pydantic.class_validators import Optional

from ftmcloud.cross_cutting.models.document import BaseDocument


class Invitation(BaseDocument):
    """
    A unique invitation to a specified organization.
    """
    pid: Optional[str]
    email: str
    organizationPid: str | None = None

    class Settings:
        name = "invitations"
        