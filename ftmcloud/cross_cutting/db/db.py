import logging

import pymongo.errors
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import TEXT

from ftmcloud.domains.data_sources.models.models import DataSource
from ftmcloud.domains.ftm_tasks.models.models import FtmTask
from ftmcloud.domains.organizations.services.organization_services import OrganizationsService
from ftmcloud.domains.privileges.services.privilege_services import PrivilegesService
from ftmcloud.domains.users.services.user_services import UserService
from ftmcloud.cross_cutting.session.session import PasswordGenerator
from ftmcloud.core.config.config import Settings
from ftmcloud.domains.attributes.models.models import Attribute
from ftmcloud.domains.categories.models.models import Category
from ftmcloud.domains.industries.models.models import Industry
from ftmcloud.domains.invitations.models.models import Invitation
from ftmcloud.domains.organizations.models.models import Organization
from ftmcloud.domains.privileges.models.models import Privilege
from ftmcloud.domains.products.models.models import Product
from ftmcloud.domains.product_types.models.models import ProductType
from ftmcloud.domains.users.models.models import User, UserContact

logger = logging.getLogger(__name__)

async def _build_indexes(motor_client: AsyncIOMotorClient):
    """ Initializes any indexes which are required to exist on application
    startup.

    :return:
    """
    logger.debug("Checking indexes...")
    indexes = [
        {
            "name": "user_contacts_search_index",
            "index": [("message", TEXT), ("subject", TEXT)],
            "table": "user_contacts"
        }
    ]

    for _index in indexes:
        logger.debug(f"Checking {_index['name']}")
        try:
            await motor_client['analytix'][_index['table']].create_index(
                _index['index'],
                name=_index["name"]
            )
            logger.info(f"Missing index {_index['name']} created on {_index['table']}.")
        except Exception as e:
            logger.error(
                f"""
                Index {_index['name']} already exists or an error occurred. {str(e)}
                """
            )
    logger.debug("Index initialization complete.")


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
            privileges = [
                Privilege(
                    pid="",
                    name="employee",
                    description="Employee role",
                    permissions=[]
                ),
                Privilege(
                    pid="",
                    name="user",
                    description="User role",
                    permissions=[]
                ),
                Privilege(
                    pid="",
                    name="reviewer",
                    description="Data reviewer role",
                    permissions=[]
                )
            ]
            default_privilege = await privilege_service.add_document(
                new_document=new_privilege
            )
            await privilege_service.insert_documents(
                documents=privileges
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
        except pymongo.errors.PyMongoError as e:
            logger.error(f"Exception during database initialization! Please restart. {str(e)}")


async def initiate_database(initial=False):
    """ Initialize the AsyncIOMotorClient.

    :param initial: bool
        whether we are performing a database initialization vs connection initiation

    :return:
    """
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.analytix,
                      document_models=[User, Privilege, Organization, Invitation, Industry, Category, Product,
                                       ProductType, Attribute, FtmTask, UserContact, DataSource])
    if initial:
        logger.info("Verifying db integrity...")
        await check_init_database(motor_client=client)
        await _build_indexes(motor_client=client)
        client.close()
        logger.info("Database integrity verified.")
