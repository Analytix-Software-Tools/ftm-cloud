from password_validator import PasswordValidator

from ftmcloud.common.auth.jwt_handler import sign_jwt, construct_user_from_aad_token
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.common.service.service import Service
from passlib.context import CryptContext
from ftmcloud.models.domains.user import User, UserProfile, UserSignIn

user_collection = User


class UserService(Service):

    def __init__(self):
        super(UserService, self).__init__(collection=User)

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
        except:
            raise FtmException("error.general.BadTokenIntegrity")
        user_exists = await self.collection.find_one(self.process_q(q=None, additional_filters={"email": update_user.email}))
        if user_exists is None:
            update_user.organization_pid = self.settings.DEFAULT_ORGANIZATION_PID
            update_user.privilege_pid = self.settings.DEFAULT_PRIVILEGE_PID
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
