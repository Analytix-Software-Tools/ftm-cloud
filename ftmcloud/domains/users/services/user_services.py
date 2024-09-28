import json

from password_validator import PasswordValidator

from ftmcloud.cross_cutting.auth.jwt_handler import sign_jwt, construct_user_from_aad_token
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.cross_cutting.notifications.email_client import EmailClient
from ftmcloud.cross_cutting.service.service import Service
from passlib.context import CryptContext
from ftmcloud.domains.users.models.models import User, UserSignIn, UserProfile, UserContact, UserContactsRepository

user_collection = User


class UserService(Service):

    def __init__(self):
        super(UserService, self).__init__(collection=User)
        self._user_contacts_repository = UserContactsRepository()

    async def notify_user(
            self,
            email,
            subject,
            message_str=None,
            message_html=None,
            attachments=None
    ):
        """ Notifies a user by email.

        :param email: str | list[str]
            the email or emails
        :param subject: str
            the subject
        :param message_str: str
            message string
        :param message_html: str
            message html
        :param attachments: list[EmailAttachment]
            the email attachment
        :return:
        """
        email_client = EmailClient()
        await email_client.send_email(
            subject=subject,
            recipients=email,
            attachments=attachments,
            html_text=message_html,
            plain_text=message_str
        )

    async def process_user_contact(self, contact_form: UserContact, sender: User):
        """ Sends the user contact notifications to admin emails and uploads
        files.

        :param contact_form: UserContact
            the user contact form submitted

        :return:
        """
        admin_users = await self.get_all(
            q=json.dumps({"privilegePid": self.settings.SUPERUSER_PRIVILEGE})
        )
        if admin_users is not None and len(admin_users) > 0:
            recipients = [_user.email for _user in admin_users]
            await self.notify_user(
                email=recipients,
                subject=f"New contact form received: {contact_form.subject}",
                message_str=f'''
                You have received a new contact form submission: \n\n\n
                Subject: {contact_form.subject}\n
                Issue Type: {contact_form.issueType}\n
                Message: {contact_form.message}\n\n\n
                User Email: {sender.email}
                User Pid: {sender.pid}
                
                ''',
                message_html=f'''
                You have received a new contact form submission:
                <br/>
                <strong>Subject</strong><br/>
                <p>{contact_form.subject}</p><br/>
                <strong>Issue Type</strong><br/>
                <p>{contact_form.issueType}</p><br/>
                <strong>Message</strong><br/>
                <p>{contact_form.message}</h1><br/>
                User Email: {sender.email}<br/><br/>
                User Pid: {sender.pid}<br/>
                '''
            )

    async def submit_user_contact(self, contact_form: UserContact):
        """ Handles a new UserContact.

        :param contact_form: UserContact
            the contact form submitted
        :return:
        """
        await self._user_contacts_repository.insert(
            new_document=contact_form
        )
        self._logger.info("New user contact form handled with issue type: {}".format(contact_form.issueType))

    async def validate_new_user(self, user):
        """
        Validates a new user to ensure their email is not taken. Hashes the
        user's password and returns the validated user.

        :param user: the user to validate
        :return: the user with validated fields
        """
        user_exists = await self.collection.find_one(User.email == user.email, {"isDeleted": {"$ne": "true"}})
        if user_exists:
            raise FtmException('error.user.InvalidEmail')
        validation_criteria = PasswordValidator()
        validation_criteria.min(8).max(100).has().lowercase().has().digits().has().no().spaces().has().symbols()
        if not validation_criteria.validate(user.password):
            raise FtmException("error.user.PasswordStrength")
        new_user = user
        hash_helper = CryptContext(schemes=["bcrypt"])
        new_user.password = hash_helper.encrypt(new_user.password)
        return new_user

    async def login_user_azure_ad(self, token):
        """
        Logs a user in via the Azure AD. For a first time sign in, decode the user's token, ensure it is valid, then
        find them by email in the database. If exists, update to match token signature otherwise create a new user
        matching the token.

        :param token: the Azure AAD token to decode
        :return: the token for the new user
        """
        try:
            update_user = construct_user_from_aad_token(token=token)
        except Exception as e:
            raise FtmException("error.general.BadTokenIntegrity")
        user_exists = await self.collection.find_one(self.process_q(q=None, additional_filters={"email": update_user.email}))
        if user_exists is None:
            update_user.organizationPid = self.settings.DEFAULT_ORGANIZATION_PID
            update_user.privilegePid = self.settings.DEFAULT_PRIVILEGE_PID
            await self.add_document(new_document=update_user)
        else:
            # TODO: Need to perform an update to the user to sync with AAD.
            update_user = user_exists
        return await sign_jwt(user=update_user)

    async def patch_users_profile(self, pid, patch_document_list):
        """
        Patches the user's own profile with information provided by them.
        """

        await self.validate_exists(pid=pid)
        for document in patch_document_list:
            if document.path == '/organizationPid' or document.path == '/privilegePid':
                raise FtmException('error.patch.InvalidPatch')

        return await self.patch(pid=pid, patch_document_list=patch_document_list)

    async def login_user(self, credentials: UserSignIn):
        """Signs a user in using the specified credentials.

        :param credentials: represents the user's credentials
        :return: a LoginResponse containing a signed access token
        """
        user_exists = await self.collection.find_one(User.email == credentials.email)
        hash_helper = CryptContext(schemes=["bcrypt"])
        if user_exists:
            password = hash_helper.verify(
                credentials.password, user_exists.password)
            if password:
                return await sign_jwt(user_exists)

            raise FtmException('error.user.InvalidCredentials')

        raise FtmException('error.user.InvalidCredentials')

    async def users_profile(self, token) -> UserProfile:
        """Retrieves the user's full profile information by returning
        their profile, the organization they are in as well as the role.

        :param token: The token to use to allocate the profile.
        :return: The user's profile.
        """
        if self.settings.AUTH_METHOD == 'Keycloak':
            user_query = {}
        else:
            user_query = {"pid": token['sub'], "isDeleted": {"$ne": True}}
        user = await self.collection.find(user_query).aggregate([{
            "$lookup":
                {
                    "from": "organizations",
                    "localField": "organizationPid",
                    "foreignField": "pid",
                    "as": "organization"
                }
        }, {
            "$lookup":
                {
                    "from": "privileges",
                    "localField": "privilegePid",
                    "foreignField": "pid",
                    "as": "privilege"
                }
        }, {
            "$addFields": {
                "privilege": {"$arrayElemAt": ["$privilege", 0]},
                "organization": {"$arrayElemAt": ["$organization", 0]},
            }
        }, {
            "$project": {
                # "_id": 0,
                # "privilege._id": 0,
                "privilege.__v": 0,
                # "organization._id": 0
            }
        }]).to_list()
        if len(user) == 0:
            raise FtmException('error.user.NotFound')
        return user[0]
