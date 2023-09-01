from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ftmcloud.core.config.config import Settings
from ftmcloud.models.attribute import Attribute
from ftmcloud.models.category import Category
from ftmcloud.models.industry import Industry
from ftmcloud.models.invitation import Invitation
from ftmcloud.models.organization import Organization
from ftmcloud.models.privilege import Privilege
from ftmcloud.models.product import Product
from ftmcloud.models.product_type import ProductType
from ftmcloud.models.student import Student
from ftmcloud.models.user import User


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.memorymaker,
                      document_models=[User, Student, Privilege, Organization, Invitation, Industry, Category, Product,
                                       ProductType, Attribute])
