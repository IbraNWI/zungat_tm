from typing import Optional
from pydantic import BaseModel, Field

class BaseConfigModel(BaseModel):
    class Config:
        populate_by_name = True



class CustomField(BaseConfigModel):
    value_type:Optional[str] = Field(None,alias="valueType")
    value:Optional[str] = Field(None,alias="value")
    type_id:Optional[str] = Field(None,alias="typeId")