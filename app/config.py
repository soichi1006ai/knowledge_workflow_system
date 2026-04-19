from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vault_root: str = "./sample_vault"
    timezone: str = "Asia/Tokyo"
    inbox_dir_name: str = "inbox"
    attachments_dir_name: str = "attachments"
    imported_dir_name: str = "system/imported"


settings = Settings()
