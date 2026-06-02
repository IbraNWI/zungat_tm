from typing import Optional
from pydantic import BaseModel, Field

class BaseConfigModel(BaseModel):
    class Config:
        populate_by_name = True


class FileField(BaseConfigModel):
    id:Optional[int] = Field(None,alias="id")
    url:Optional[str] = Field(None,alias="url")
    name:Optional[str] = Field(None,alias="filename")
    file:Optional[bytes] = Field(None,alias="content")

class CustomField(BaseConfigModel):
    value_type:Optional[str] = Field(None,alias="valueType")
    value:Optional[str] = Field(None,alias="value")
    type_id:Optional[str] = Field(None,alias="typeId")