from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.tm_driver.lib.schemas.operation import Operation

class TMOperationError(Exception):
    pass

class MakeOperation:
    def __init__(self,tm_client:TMClient):
        self.tm_client = tm_client

    def _getOperation(self,fact_payment,payment_rule):
        return Operation(
            driver_id=payment_rule.driver_id,
            oper_sum=fact_payment.opportunity,
            oper_type="receipt",
            title="Тестовая отмена платежа Zungat"
            )
    
    def make(self,fact_payment,payment_rule):
        operation = self._getOperation(fact_payment,payment_rule)
        operation = self.tm_client.operation.add(operation)
        return operation