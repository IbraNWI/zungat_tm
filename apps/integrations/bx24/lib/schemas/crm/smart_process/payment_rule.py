from typing import Optional, List

from pydantic import Field,field_validator

from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel



class PaymentRule(BaseConfigModel):
    id:Optional[int] = Field(None,alias="id")
    title:Optional[str] = Field(None,alias="title")
    created_time:Optional[str] = Field(None,alias="createdTime")
    company_id:Optional[int] = Field(None,alias="companyId")
    contact_id:Optional[int] = Field(None,alias="contactId")
    contact_ids:Optional[List[int]] = Field(None,alias="contactIds")
    deal_id:Optional[int] = Field(None,alias="parentId2")
    category_id:Optional[int] = Field(None,alias="categoryId")
    stage_id:Optional[str] = Field(None,alias="stageId")
    assigned_by_id:Optional[int] = Field(None,alias="assignedById")
    driver_id:Optional[int] = Field(None,alias="ufCrm15DriversNumber")
    payment_sum:Optional[float] = Field(None,alias="ufCrm15_1753599639155")
    first_pay_date:Optional[str] = Field(None,alias="ufCrm15_1757831335159")
    last_payment_date:Optional[str] = Field(None,alias="ufCrm15_1753616129036")
    is_active:Optional[int] = Field(None,alias="ufCrm15RuleState")
    allow_overdraft:Optional[bool] = Field(None,alias="ufCrm15AllowOverdraft")
    payment_frequency:Optional[int] = Field(None,alias="ufCrm15_1753599678264")
    payment_day_time:Optional[int] = Field(None,alias="ufCrm15PaymentDayTime")
    arested_date:Optional[str] = Field(None,alias="ufCrm15ArestedDate")


    @field_validator("payment_sum", mode="before")
    @classmethod
    def extract_numeric_part(cls, value):

        if isinstance(value, str):
            if value == "":
                return None
            else:
                return float(value.split("|")[0])

        return value

