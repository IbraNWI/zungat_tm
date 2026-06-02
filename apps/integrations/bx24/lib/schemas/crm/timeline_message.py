from typing import Optional
from datetime import datetime
from pydantic import Field
from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel



class TimelineMessage(BaseConfigModel):
    message_id:Optional[int] = Field(None,alias="id")
    entity_type_id:Optional[str] = Field(None,alias="entityTypeId")
    entity_id:Optional[int] = Field(None,alias="entityId")
    created_time:Optional[datetime] = Field(None,alias="created")
    author_id:Optional[int] = Field(None,alias="authorId")
    title:Optional[str] = Field(None,alias="title")
    text:Optional[str] = Field(None,alias="text")
    icon_code:Optional[str] = Field(None,alias="iconCode")