import base64
import os
from typing import Optional

from pydantic import BaseSettings

from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "FtmCloud"
    API_REVISION: str = "v0"
    DEBUG: bool = False

    # Database
    MONGO_URI = base64.b64decode(os.environ['MONGO_URI_ENCODED']) if "MONGO_URI_ENCODED" in \
                                                                     os.environ else 'mongodb://mongodb:27017'
    DATABASE_URL: Optional[str] = MONGO_URI
    MAX_QUERY_LIMIT: int = 100
    DEFAULT_QUERY_LIMIT: int = 10

    # JWT
    secret_key: str = 'D(G+KbPe'
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        orm_mode = True


# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
