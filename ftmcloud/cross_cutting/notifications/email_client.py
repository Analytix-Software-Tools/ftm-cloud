import base64
import logging
from venv import logger

from pydantic.class_validators import validator
from pydantic.main import BaseModel
from azure.communication.email import EmailClient as AzureEmailClient

from ftmcloud.core.config.config import Settings


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
        self.settings = Settings()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._email_client = AzureEmailClient.from_connection_string(
            conn_str=self.settings.AZURE_COMMUNICATION_URI
        )

    async def send_email(
            self,
            subject: str,
            recipients: str | list[str],
            sender_email: str='DoNotReply@analytix-ai.com',
            attachments: list[EmailAttachment] | None = None,
            plain_text: str | None = None,
            html_text: str | None = None
    ):
        """ Send notification email to the specified address.

        :param subject: str
            subject of message
        :param recipients: str | list[str]
            single email or list of target emails to send to
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
        if self.settings.AZURE_COMMUNICATION_URI == '':
            return self._logger.warning(
                msg=f'''
                    Variable {self.settings.AZURE_COMMUNICATION_URI.__name__} is unset. Outgoing email request
                    will be ignored.
                '''
            )
        try:
            if isinstance(recipients, str):
                mailto_list = [recipients]
            else:
                mailto_list = []
                for _recipient in recipients:
                    mailto_list.append({'address': _recipient})
            content = {
                'subject': subject
            }
            if plain_text is not None:
                content['plainText'] = plain_text
            if html_text is not None:
                content['htmlText'] = html_text
            message = {
                'senderAddress': sender_email,
                'recipients': {
                    'to': mailto_list
                },
                'content': content,
            }
            self._logger.info(
                f'''
                Sending email with subject {subject} to {len(recipients) if isinstance(recipients, list) else 1}
                recipients.
                '''
            )
            poller = self._email_client.begin_send(
                message
            )
            result = poller.result()
            self._logger.info(
                f'''
                Email sent successfully!
                '''
            )
            return result
        except Exception as e:
            self._logger.error(
                msg=f'''
                    Email client encountered an exception attempting to send message:
                    {str(e)}
                '''
            )
