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
    SUPERUSER_PRIVILEGE: str = "58f29fb3-3759-4b86-b4a2-cdc0b3b0538e"
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
    MONGO_URI = base64.b64decode(os.environ['MONGO_URI_ENCODED']).decode('utf-8') if "MONGO_URI_ENCODED" in \
                                                                     os.environ else base64.b64decode(
        'bW9uZ29kYitzcnY6Ly9hZG1pbjpla3kwUFF5TjNjZDcxV3dZQGNsdXN0ZXIwLmlsbHFoLm1vbmdvZGIubmV0').decode('utf-8')
    DATABASE_URL: Optional[str] = MONGO_URI
    AUTH_METHOD = os.environ['AUTHENTICATION_METHOD'] if 'AUTHENTICATION_METHOD' in \
                                                         os.environ else "azure"

    DEFAULT_PRIVILEGE_NAME = "reviewer"
    DEFAULT_ORGANIZATION_PID = "2022eb7c-7abd-4d25-9e4e-d67820b9a5bd"

    ELASTICSEARCH_API_KEY_ENCODED = os.environ['ELASTICSEARCH_API_KEY_ENCODED'] if "ELASTICSEARCH_API_KEY_ENCODED" in os.environ \
        else 'bW9uZ29kYitzcnY6Ly9hZG1pbjpla3kwUFF5TjNjZDcxV3dZQGNsdXN0ZXIwLmlsbHFoLm1vbmdvZGIubmV0'
    ELASTICSEARCH_API_KEY = base64.b64decode(ELASTICSEARCH_API_KEY_ENCODED).decode('utf-8')

    ELASTICSEARCH_URI_ENCODED = os.environ['ELASTICSEARCH_URI_ENCODED'] if "ELASTICSEARCH_URI_ENCODED" in os.environ \
        else 'aHR0cHM6Ly9sb2NhbGhvc3Q6OTIwMC8='
    ELASTICSEARCH_URI = base64.b64decode(ELASTICSEARCH_URI_ENCODED).decode('utf-8')

    AZURE_COMMUNICATION_URI_ENCODED = os.getenv('AZURE_COMMUNICATION_URI_ENCODED', '')
    AZURE_COMMUNICATION_URI = base64.b64decode(AZURE_COMMUNICATION_URI_ENCODED).decode('utf-8') if AZURE_COMMUNICATION_URI_ENCODED is not '' else ''

    # JWT
    JWT_SECRET = os.environ.get("JWT_SECRET", 'D(G+KbPe')
    secret_key: str = JWT_SECRET


# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
