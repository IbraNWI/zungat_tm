from typing import Optional, List
from datetime import datetime

from pydantic import Field,field_validator

from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel



class PlanPayment(BaseConfigModel):
    id:Optional[int] = Field(None,alias="id")
    title:Optional[str] = Field(None,alias="title")
    created_time:Optional[datetime] = Field(None,alias="createdTime")
    company_id:Optional[int] = Field(None,alias="companyId")
    contact_id:Optional[int] = Field(None,alias="contactId")
    contact_ids:Optional[List[int]] = Field(None,alias="contactIds")
    category_id:Optional[int] = Field(None,alias="categoryId")
    stage_id:Optional[str] = Field(None,alias="stageId")
    assigned_ny_id:Optional[int] = Field(None,alias="assignedById")
    opportunity:Optional[float] = Field(None,alias="opportunity")
    payed_sum:Optional[float] = Field(None,alias="ufCrm7_1751799934475")

    @field_validator("payed_sum", mode="before")
    @classmethod
    def extract_numeric_part(cls, value):

        if isinstance(value, str):
            if value == "":
                return None
            else:
                return float(value.split("|")[0])

        return value

