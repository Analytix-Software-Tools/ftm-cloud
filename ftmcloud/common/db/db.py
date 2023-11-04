from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

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
from ftmcloud.models.domains.user import User


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.memorymaker,
                      document_models=[User, Privilege, Organization, Invitation, Industry, Category, Product,
                                       ProductType, Attribute, ModelConfiguration])