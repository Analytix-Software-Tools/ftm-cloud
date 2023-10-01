from beanie import init_beanie
from beanie.odm.models import BaseModel
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


class Repository:

    # Represents the target collection model.
    model_collection = None

    def __init__(self, model_collection: BaseModel):
        """
        A Repository represents an abstraction of a collection of models. The repository's intent is to abstract
        the data access functionality from the target to ensure queries are performant at the lowest level and
        adhere to the data system.
        """
        self.model_collection = model_collection

    def replace_one(self, match_query, new_document):
        """
        Replaces the document matching the specified query.

        :param match_query:
        :param new_document:
        :return:
        """
        pass

    def update_one(self, query):
        pass

    def insert(self, new_document):
        pass
