from password_validator import PasswordValidator

from ftmcloud.core.auth.jwt_handler import sign_jwt
from ftmcloud.core.exception.exception import FtmException
from ftmcloud.core.service import Service
from passlib.context import CryptContext
from ftmcloud.models.domains.users.user import User, UserProfile, UserSignIn

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
