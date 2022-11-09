from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from models.attribute import Attribute
from models.organization import Organization
from models.industry import Industry
from models.privilege import Privilege
from models.service import Service
from models.service_classification import ServiceClassification
from models.user import User
from models.student import Student


class Settings(BaseSettings):
    # database configurations
    # DATABASE_URL: Optional[str] = 'mongodb+srv://admin:eky0PQyN3cd71WwY@cluster0.illqh.mongodb.net'
    DATABASE_URL: Optional[str] = 'mongodb://mongodb:27017'
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
                      document_models=[User, Student, Privilege, Organization, Industry, ServiceClassification, Service,
                                       Attribute])
