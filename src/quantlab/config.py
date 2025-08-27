from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    tushare_token: str = ""
    feishu_webhook: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
