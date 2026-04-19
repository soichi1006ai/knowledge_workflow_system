from typing import Optional

from pydantic import BaseModel, ConfigDict


class KOSBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class ApiResponse(KOSBaseModel):
    ok: bool = True
    message: Optional[str] = None
