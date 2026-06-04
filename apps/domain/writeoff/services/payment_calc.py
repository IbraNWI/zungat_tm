
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient

class CalculateError(Exception):
    pass

class PaymentCalculation:
    def __init__(self,tm_client:TMClient):
        self.tm_client = tm_client


    def _allowOverdraft(self,payment_rule,arest_amount):
        if payment_rule.allow_overdraft is False and arest_amount > 0:
            raise CalculateError("Don't allow overdraft")

    def calculate(self,fact_payment,payment_rule):
        balance = self.tm_client.driver.get(id=payment_rule.driver_id).balance
        requested = fact_payment.opportunity

        if balance >= requested:
            return requested, 0

        paid = max(balance, 0)
        arrest = requested - paid

        self._allowOverdraft(payment_rule, arrest)

        return paid, arrest