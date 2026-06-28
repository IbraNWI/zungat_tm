from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.domain.autopayment.schemas.installment import Installment
from apps.integrations.tm_driver.lib.schemas import Operation
from apps.integrations.bx24.lib.schemas import FactPayment


class CalculateError(Exception):
    pass

class InstallmentCalculation:
    def __init__(self,tm_client:TMClient):
        self.tm_client = tm_client
    
    def _getPaymentSum(self,installment:Installment) -> float:
        deal = installment.deal
        payment_sum = installment.payment_rule.payment_sum
        
        allow_payment_sum = deal.opportunity if deal.opportunity is not None else 0
        arest_sum = deal.total_arest_sum if deal.total_arest_sum is not None else 0
        pay_sum = deal.installment_pay_sum if deal.installment_pay_sum is not None else 0
        
        allow_payment_sum -= (arest_sum + pay_sum)
        
        if allow_payment_sum <= 0:
            return 0
        elif allow_payment_sum < payment_sum:
            return round(allow_payment_sum,2)
        else:
            return round(payment_sum,2)
 
    def _makeOperation(self,installment:Installment,payment_sum:float):
        return Operation(
            driver_id=installment.payment_rule.driver_id,
            oper_sum=payment_sum,
            oper_type="expense",
            title="Автоматическое списание. Зунгат"
            )
    
    def _makePayment(self,installment:Installment,balance:float):
        requested = installment.operation.oper_sum

        if balance >= requested:
            paid = requested
            arrest = 0
        else:
            paid = max(balance, 0)
            arrest = requested - paid

        return FactPayment(
            title="Автоматическое списание. Зунгат-Тешам",
            contact_ids=installment.payment_rule.contact_ids,
            category_id=15,
            stage_id="DT1052_15:SUCCESS",
            assigned_by_id=1,
            created_by_id=1,
            opportunity=round(paid,2),
            arest_sum=round(arrest,2),
            payment_type_id=249,
            deal_id=installment.payment_rule.deal_id,        
            )

    def calculate(self,installments:list[Installment]):
        for installment in installments:
            balance = self.tm_client.driver.get(installment.payment_rule.driver_id).balance
            payment_sum = self._getPaymentSum(installment)
            installment.operation = self._makeOperation(installment,payment_sum)
            installment.fact_payment = self._makePayment(installment,balance)
        
        return installments