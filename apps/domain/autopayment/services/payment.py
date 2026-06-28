from datetime import datetime
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.domain.autopayment.schemas.installment import Installment
from apps.integrations.bx24.lib.schemas import FactPayment,PaymentRule


class CreatePaymentError(Exception):
    pass

class CreatePayment:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client

    

    def _updatePaymentRule(self,installment:Installment):
        installment.fact_payment.tm_payment_id = installment.operation.id
        return installment
    
    def _createFactPayment(self,installment:Installment):
        try:
            fact_payment = self.bx_client.fact_payment.add(installment.fact_payment)
        except:
            # Не получилось создать платеж
            ...
        installment.fact_payment = fact_payment
        return installment


    def create(self,installments:list[Installment]):
        for installment in installments:
            installment = self._updatePaymentRule(installment)
            installment = self._createFactPayment(installment)
            print("Создание платежа по рассрочке:",installment.fact_payment.id)
        return installments
