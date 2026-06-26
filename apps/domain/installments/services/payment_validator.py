from typing import List
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.bx24.lib.schemas import PaymentRule


class ValidationError(Exception):
    pass


class PaymentValidator:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client
    

    def _validatePaymentRules(payment_rules:List[PaymentRule]):
        ...