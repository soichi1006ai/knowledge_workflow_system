from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vault_root: str = "./sample_vault"
    timezone: str = "Asia/Tokyo"


settings = Settings()
