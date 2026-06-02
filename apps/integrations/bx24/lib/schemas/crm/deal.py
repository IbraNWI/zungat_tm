from typing import Optional, List
from datetime import datetime

from pydantic import Field,field_validator

from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel, CustomField



class Deal(BaseConfigModel):
    id:Optional[int] = Field(None,alias="id")
    title:Optional[str] = Field(None,alias="title")
    category_id:Optional[int] = Field(None,alias="categoryId")
    stage_id:Optional[str] = Field(None,alias="stageId")
    opportunity:Optional[float] = Field(None,alias="opportunity")
    created_time:Optional[datetime] = Field(None,alias="createdTime")
    begin_date:Optional[datetime] = Field(None,alias="begindate")
    close_date:Optional[datetime] = Field(None,alias="closedate")
    assigned_by_id:Optional[int] = Field(None,alias="assignedById")

    company_id:Optional[int] = Field(None,alias="companyId")
    contact_id:Optional[int] = Field(None,alias="contactId")
    contact_ids:Optional[List[int]] = Field(None,alias="contactIds")

    # CustomFields
    installment_pay_sum:Optional[float] = Field(None,alias="ufCrm_1752852537")
    total_arest_sum:Optional[float] = Field(None,alias="ufCrm_1755696720")
    payment_rule:Optional[int] = Field(None,alias="ufCrm_1753602610")


    @field_validator("installment_pay_sum","total_arest_sum", mode="before")
    @classmethod
    def extract_numeric_part(cls, value):

        if isinstance(value, str):
            return float(value.split("|")[0])

        return value