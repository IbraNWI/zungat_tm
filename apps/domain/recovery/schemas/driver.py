from typing import Optional
from pydantic import BaseModel

from apps.integrations.bx24.lib.schemas import (
    Deal,FactPayment,PaymentRule
)
from apps.integrations.tm_driver.lib.schemas import Operation

class BaseConfigModel(BaseModel):
    class Config:
        populate_by_name = True

class Installment(BaseConfigModel):
    payment_rule:Optional[PaymentRule] = None
    deal:Optional[Deal] = None
    fact_payment:Optional[FactPayment] = None


class Driver(BaseConfigModel):
    driver_id:Optional[int] = None
    installments:list[Installment] = []
    operations:list[Operation] = []