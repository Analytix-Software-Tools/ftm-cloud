import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ftmcloud.domains.organizations.services.organization_services import OrganizationsService
from ftmcloud.domains.privileges.services.privilege_services import PrivilegesService
from ftmcloud.domains.users.services.user_services import UserService
from ftmcloud.common.session.session import PasswordGenerator
from ftmcloud.core.config.config import Settings
from ftmcloud.models.domains.attribute import Attribute
from ftmcloud.models.domains.category import Category
from ftmcloud.models.domains.industry import Industry
from ftmcloud.models.domains.invitation import Invitation
from ftmcloud.models.domains.model_configuration import ModelConfiguration
from ftmcloud.models.domains.organization import Organization
from ftmcloud.models.domains.privilege import Privilege
from ftmcloud.models.domains.product import Product
from ftmcloud.models.domains.product_type import ProductType
from ftmcloud.models.domains.task import Task
from ftmcloud.models.domains.user import User


async def _build_indexes(motor_client: AsyncIOMotorClient):
    """ Performs initialization to build indexes.

    :return:
    """
    # motor_client
    pass


async def check_init_database(motor_client: AsyncIOMotorClient):
    """ Check whether database requires initialization. Requires
    initialization if

    1. There is no administrative role.
    2. There are no users satisfying the administrative role.

    :param motor_client:
    :return:
    """
    privilege_service = PrivilegesService()
    admin_privilege = await privilege_service.find_one(
        {"name": "developer"}
    )
    if admin_privilege is None:
        logger = logging.getLogger(__name__)
        logger.info(f"Database flagged for initializing. Performing initial migration...")
        try:
            users_service = UserService()
            organizations_service = OrganizationsService()
            new_privilege = Privilege(
                pid="",
                name="developer",
                description="Administrator role",
                permissions=[]
            )
            default_privilege = await privilege_service.add_document(
                new_document=new_privilege
            )
            default_organization = Organization(
                name="Default",
                description="Default organization"
            )
            default_org = await organizations_service.add_document(
                new_document=default_organization
            )
            pwd_generator = PasswordGenerator(length=16)
            random_pass = pwd_generator.generate()
            new_user = User(
                email="testuser@email.com",
                firstName="Default",
                lastName="User",
                password=random_pass,
                privilegePid=default_privilege.pid,
                organizationPid=default_org.pid
            )
            await users_service.validate_new_user(
                user=new_user
            )
            await users_service.add_document(
                new_document=new_user
            )
            logger.info(
                f"""
                Database initialization complete. User: {new_user.email}, Password: {random_pass}. 
                Please ensure you save these credentials! You will not be able to retrieve them later.
                """
            )
        except Exception as e:
            logger.error(f"Exception during database initialization! Please restart. {str(e)}")


async def initiate_database():
    """ Initialize the AsyncIOMotorClient.

    :return:
    """
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.analytix,
                      document_models=[User, Privilege, Organization, Invitation, Industry, Category, Product,
                                       ProductType, Attribute, ModelConfiguration, Task])
    await check_init_database(motor_client=client)
