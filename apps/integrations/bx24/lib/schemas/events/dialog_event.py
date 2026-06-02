from typing import Optional
from pydantic import Field
from .base_config import BaseConfigModel

class Connector(BaseConfigModel):
    connector_id:Optional[str] = Field(None,alias="connector_id")
    line_id:Optional[str] = Field(None,alias="line_id")
    chat_id:Optional[str] = Field(None,alias="chat_id")
    user_id:Optional[str] = Field(None,alias="user_id")

class Chat(BaseConfigModel):
    chat_id:Optional[str] = Field(None,alias="chat_id")

class Line(BaseConfigModel):
    id:Optional[str] = Field(None,alias="id")
    name:Optional[str] = Field(None,alias="name")

class Dialog(BaseConfigModel):
    connector:Optional[Connector] = Field(None,alias="connector")
    chat:Optional[Chat] = Field(None,alias="chat")
    line:Optional[Line] = Field(None,alias="line")