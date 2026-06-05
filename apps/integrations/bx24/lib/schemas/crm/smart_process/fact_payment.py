from typing import Optional, List
from datetime import datetime

from pydantic import Field,field_validator

from apps.integrations.bx24.lib.schemas.crm.base_model import BaseConfigModel


# {'ID': '253', 'VALUE': 'Ручной платеж'}, {'ID': '275', 'VALUE': 'Первый взнос'}, {'ID': '255', 'VALUE': 'Ручное списание ТМ'}, {'ID': '249', 'VALUE': 'Автосписание ТМ'}, {'ID': '251', 'VALUE': 'Списание долга ТМ'}



payment_types = {
    "FIRST_PAYMENT":275,

    }
class PaymentStates:
    ACCEPT = 285
    CENCELED = 287
    NOT_PROCESSED = 289


class FactPaymentInfo:
    payment_types = PaymentStates



class FactPayment(BaseConfigModel):
    id:Optional[int] = Field(None,alias="id")
    title:Optional[str] = Field(None,alias="title")
    created_time:Optional[datetime] = Field(None,alias="createdTime")
    company_id:Optional[int] = Field(None,alias="companyId")
    contact_id:Optional[int] = Field(None,alias="contactId")
    contact_ids:Optional[List[int]] = Field(None,alias="contactIds")
    category_id:Optional[int] = Field(None,alias="categoryId")
    stage_id:Optional[str] = Field(None,alias="stageId")
    assigned_by_id:Optional[int] = Field(None,alias="assignedById")
    opportunity:Optional[float] = Field(None,alias="opportunity")
    arest_sum:Optional[float] = Field(None,alias="ufCrm9_1755697433")
    payment_type_id:Optional[int] = Field(None,alias="ufCrm9PaymentType")
    tm_payment_id:Optional[int] = Field(None,alias="ufCrm9TmPaymentId")
    payment_state_id:Optional[int] = Field(None,alias="ufCrm9PaymentState")
    deal_id:Optional[int] = Field(None,alias="parentId2")
    comment:Optional[str] = Field(None,alias="comments")

    @field_validator("arest_sum", mode="before")
    @classmethod
    def extract_numeric_part(cls, value):

        if isinstance(value, str):
            if value == "":
                return None
            else:
                return float(value.split("|")[0])

        return value