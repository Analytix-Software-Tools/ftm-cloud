import base64
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
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    MONGO_URI = 'mongodb://mongodb:27017'
    if 'MONGO_URI_ENCODED' in os.environ:
        MONGO_URI = base64.b64decode(os.environ['MONGO_URI_ENCODED'])
    DATABASE_URL: Optional[str] = MONGO_URI
    MAX_QUERY_LIMIT: int = 100
    DEFAULT_QUERY_LIMIT: int = 10

    # JWT
    secret_key: str = 'D(G+KbPe'
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        orm_mode = True


limiter = Limiter(key_func=get_remote_address)


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.memorymaker,
                      document_models=[User, Student, Privilege, Organization, Industry, Category, Product, ProductType,
                                       Attribute])
