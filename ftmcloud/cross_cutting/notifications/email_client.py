import base64

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from azure.communication.email import EmailClient as AzureEmailClient


class EmailAttachment(BaseModel):
    """
    Email attachment model.
    """
    name: str
    attachment_type: str
    content: bytes

    @validator("content")
    def validate_file_format(cls, v):
        """ Convert the file to the formatting requested
        by the underlying client.

        :param v: Any
            the incoming value

        :return: bytes
            the file bytes, encoded in base64
        """
        file_bytes_b64 = base64.b64encode(bytes(v, 'utf-8'))
        return file_bytes_b64


class EmailClient:

    _email_client = None

    def __init__(self):
        """
        Provides communication via email to send notifications
        to users.
        """
        self._email_client = AzureEmailClient.from_connection_string(
            conn_str=""
        )

    async def send_email(
            self,
            subject: str,
            target_email: str,
            sender_email: str,
            attachments: list[EmailAttachment] | None = None,
            plain_text: str | None = None,
            html_text: str | None = None
    ):
        """ Send notification email to the specified address.

        :param subject: str
            subject of message
        :param target_email: str
            target email
        :param sender_email: str
            sender email
        :param attachments: list[EmailAttachment]
            attachments to include
        :param plain_text: str
            plaintext body
        :param html_text: str
            html body
        :return:
        """
        message = {

        }
        poller = await self._email_client.begin_send(
            message
        )
        result = await poller.result()
        return result
