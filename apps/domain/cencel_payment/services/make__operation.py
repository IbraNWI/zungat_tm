from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.tm_driver.lib.schemas.operation import Operation

class TMOperationError(Exception):
    pass

class MakeOperation:
    def __init__(self,tm_client:TMClient):
        self.tm_client = tm_client

    def _getOperation(self,fact_payment,payment_rule):
        oper_sum =  fact_payment.opportunity + fact_payment.arest_sum
        return Operation(
            driver_id=payment_rule.driver_id,
            oper_sum=oper_sum,
            oper_type="receipt",
            title=f"Отмена платежа {fact_payment.tm_payment_id}. Зунгат"
            )
    
    def make(self,fact_payment,payment_rule):
        operation = self._getOperation(fact_payment,payment_rule)
        operation = self.tm_client.operation.add(operation)
        return operation