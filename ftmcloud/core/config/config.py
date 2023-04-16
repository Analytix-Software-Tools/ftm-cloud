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
    SUPERUSER_PRIVILEGE: str = "aefbe39c-2a12-471d-bd32-3a631f67c179"

    # Database
    MONGO_URI = base64.b64decode(os.environ['MONGO_URI_ENCODED']) if "MONGO_URI_ENCODED" in \
                                                                     os.environ else base64.b64decode('bW9uZ29kYitzcnY6Ly9hZG1pbjpla3kwUFF5TjNjZDcxV3dZQGNsdXN0ZXIwLmlsbHFoLm1vbmdvZGIubmV0')
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
