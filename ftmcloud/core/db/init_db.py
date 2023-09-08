from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ftmcloud.core.config.config import Settings
from ftmcloud.models.domains.attributes.attribute import Attribute
from ftmcloud.models.domains.categories.category import Category
from ftmcloud.models.domains.industries.industry import Industry
from ftmcloud.models.domains.invitations.invitation import Invitation
from ftmcloud.models.domains.organizations.organization import Organization
from ftmcloud.models.domains.privileges.privilege import Privilege
from ftmcloud.models.domains.products.product import Product
from ftmcloud.models.domains.product_types.product_type import ProductType
from ftmcloud.models.domains.users.user import User


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.memorymaker,
                      document_models=[User, Privilege, Organization, Invitation, Industry, Category, Product,
                                       ProductType, Attribute])
