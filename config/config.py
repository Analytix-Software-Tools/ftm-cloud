from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from models.gallery import Gallery
from models.organization import Organization
from models.industry import Industry
from models.privilege import Privilege
from models.user import User
from models.student import Student


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = 'mongodb://localhost/'
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
                      document_models=[User, Student, Privilege, Organization, Gallery, Industry])
