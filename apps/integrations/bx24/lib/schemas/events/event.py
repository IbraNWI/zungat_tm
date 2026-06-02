from typing import Optional
from pydantic import Field
from .base_config import BaseConfigModel


class Event(BaseConfigModel):
    event:Optional[str] = Field(None,alias="event")
    handler:Optional[str] = Field(None,alias="handler")
    auth_type:Optional[str] = Field(None,alias="auth_type")
    offline:Optional[int] = Field(None,alias="offline")