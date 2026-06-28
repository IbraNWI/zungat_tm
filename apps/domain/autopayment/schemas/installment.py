from typing import Optional, List
from pydantic import BaseModel, Field

from apps.integrations.bx24.lib.schemas import (
    Deal,PaymentRule,FactPayment
)
from apps.integrations.tm_driver.lib.schemas import Operation

class BaseConfigModel(BaseModel):
    class Config:
        populate_by_name = True



class Installment(BaseConfigModel):
    deal:Optional[Deal] = None
    payment_rule:Optional[PaymentRule] = None
    operation:Optional[Operation] = None
    fact_payment:Optional[FactPayment] = None