from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Extra


class Settings(BaseSettings):
    secret_key: str
    token_exp_time_min: int
    token_crypt_algorithm: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow
        env_prefix = "MN_"


settings = Settings()

