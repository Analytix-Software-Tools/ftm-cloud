import os
from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from models.attribute import Attribute
from models.organization import Organization
from models.industry import Industry
from models.privilege import Privilege
from models.product import Product
from models.product_type import ProductType
from models.category import Category
from models.user import User
from models.student import Student


class Settings(BaseSettings):
    # database configurations
    # 'mongodb+srv://admin:eky0PQyN3cd71WwY@cluster0.illqh.mongodb.net'
    DATABASE_URL: Optional[str] =  os.environ['MONGO_URI_PROD_ENCODED'] if 'MONGO_URI_PROD_ENCODED' in os.environ else 'mongodb://mongodb:27017'
    MAX_QUERY_LIMIT: int = 100

    # JWT
    secret_key: str = 'D(G+KbPe'
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        orm_mode = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.memorymaker,
                      document_models=[User, Student, Privilege, Organization, Industry, Category, Product, ProductType,
                                       Attribute])
