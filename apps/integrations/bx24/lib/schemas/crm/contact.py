from typing import Optional, List, Union
from pydantic import Field

from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel, CustomField



class Contact(BaseConfigModel):
    id:Optional[int] = Field(None,alias="ID")
    name:Optional[str] = Field(None,alias="name")
    second_name:Optional[str] = Field(None,alias="secondName")
    last_name:Optional[str] = Field(None,alias="lastName")
    birth_date:Optional[str] = Field(None,alias="birthdate")
    post:Optional[str] = Field(None,alias="post")
    contact_type:Optional[str] = Field(None,alias="typeId")
    date_create:Optional[str] = Field(None,alias="dateCreate")
    date_modify:Optional[str] = Field(None,alias="dateModify")
    opened:Optional[str] = Field(None,alias="opened")
    source_id:Optional[str] = Field(None,alias="sourceId")
    source_description:Optional[str] = Field(None,alias="sourceDescription")
    observers:Optional[List[int]] = Field(None,alias="observers")

    has_phone:Optional[str] = Field(None,alias="hasPhone")
    fm:Optional[List[CustomField]] = Field(None,alias="fm")
    web:Optional[List[CustomField]] = Field(None,alias="web")
    
    address_country:Optional[str] = Field(None,alias="addressCountry")
    address_province:Optional[str] = Field(None,alias="addressProvince")
    address_city:Optional[str] = Field(None,alias="addressCity")

    # UTM 
    utm_source:Optional[str] = Field(None,alias="utmSource")
    utm_medium:Optional[str] = Field(None,alias="utmMedium")
    utm_campaign:Optional[str] = Field(None,alias="utmCompaign")
    utm_content:Optional[str] = Field(None,alias="utmContent")

    # Custom fields
    driver_id:Optional[int] = Field(None,alias="ufCrm_1727700536348")
    balance:Optional[float] = Field(None,alias="ufCrm_1729781383")

    


