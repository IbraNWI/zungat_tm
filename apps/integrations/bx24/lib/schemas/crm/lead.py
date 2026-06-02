from typing import Optional, List, Union
from pydantic import Field
from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel, CustomField



class Lead(BaseConfigModel):
    id:Optional[int] = Field(None,alias="id")
    title:Optional[str] = Field(None,alias="title")
    contact_ids:Optional[List[int]] = Field(None,alias="contactIds")
    stage_id:Optional[str] = Field(None,alias="stageId")
    opportunity:Union[None,str,float] = Field(None,alias="opportunity")

    name:Optional[str] = Field(None,alias="name")
    second_name:Optional[str] = Field(None,alias="secondName")
    last_name:Optional[str] = Field(None,alias="lastName")
    source:Optional[str] = Field(None,alias="sourceId")
    birth_date:Optional[str] = Field(None,alias="birthdate")
    fm:Optional[List[CustomField]] = Field(None,alias="fm")
    source_id:Union[int,str,None] = Field(None,alias="sourceId")