import base64
import os
from typing import Optional

from pydantic import BaseSettings

from slowapi import Limiter
from slowapi.util import get_remote_address


class BaseConfig(BaseSettings):
    PROJECT_NAME: str = "FtmCloud"
    API_REVISION: str = "v0"
    DEBUG: bool = False
    SUPERUSER_PRIVILEGE: str = "aefbe39c-2a12-471d-bd32-3a631f67c179"
    MAX_QUERY_LIMIT: int = 100
    DEFAULT_QUERY_LIMIT: int = 10
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        orm_mode = True


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class Settings(BaseConfig):
    # Database
    MONGO_URI = base64.b64decode(os.environ['MONGO_URI_ENCODED']) if "MONGO_URI_ENCODED" in \
                                                                     os.environ else base64.b64decode(
        'bW9uZ29kYitzcnY6Ly9hZG1pbjpla3kwUFF5TjNjZDcxV3dZQGNsdXN0ZXIwLmlsbHFoLm1vbmdvZGIubmV0')
    DATABASE_URL: Optional[str] = MONGO_URI
    AUTH_METHOD = os.environ['AUTHENTICATION_METHOD'] if 'AUTHENTICATION_METHOD' in \
                                                         os.environ else "mongo"

    PRIVILEGE_NAME_MAPPING = {}

    ELASTICSEARCH_API_KEY_ENCODED = os.environ['ELASTICSEARCH_API_KEY_ENCODED'] if "ELASTICSEARCH_API_KEY_ENCODED" in os.environ \
        else 'bW9uZ29kYitzcnY6Ly9hZG1pbjpla3kwUFF5TjNjZDcxV3dZQGNsdXN0ZXIwLmlsbHFoLm1vbmdvZGIubmV0'
    ELASTICSEARCH_API_KEY = base64.b64decode(ELASTICSEARCH_API_KEY_ENCODED).decode('utf-8')

    ELASTICSEARCH_URI_ENCODED = os.environ['ELASTICSEARCH_URI_ENCODED'] if "ELASTICSEARCH_URI_ENCODED" in os.environ \
        else 'bW9uZ29kYitzcnY6Ly9hZG1pbjpla3kwUFF5TjNjZDcxV3dZQGNsdXN0ZXIwLmlsbHFoLm1vbmdvZGIubmV0'
    ELASTICSEARCH_URI = base64.b64decode(ELASTICSEARCH_URI_ENCODED).decode('utf-8')

    # JWT
    JWT_SECRET = os.environ.get("JWT_SECRET", 'D(G+KbPe')
    secret_key: str = JWT_SECRET


# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
