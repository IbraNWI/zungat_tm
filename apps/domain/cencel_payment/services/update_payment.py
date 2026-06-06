from datetime import datetime
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.bx24.lib.schemas import FactPayment,PaymentRule

class UpdatePaymentError(Exception):
    pass

class UpdatePayment:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client

    

    def _updatePaymentRule(self,payment_rule):
        self.bx_client.payment_rule.update(PaymentRule(
            id=payment_rule.id,
            last_payment_date=datetime.now().strftime("%d.%m.%Y")
            )
        )
        return payment_rule
    
    def _updateFactPayment(self,
                           fact_payment_id:int,
                           operation:any,
                           cenceled_tm_payment_id:int):  
                      
        self.bx_client.fact_payment.update(FactPayment(
            id=fact_payment_id,
            tm_payment_id=operation.id,
            stage_id="DT1052_15:SUCCESS",
            tm_payment_id=operation.id,
            cenceled_tm_payment_id=cenceled_tm_payment_id
                )
            )
    
    def updateFatalError(self,fact_payment):
        ...

    def updateRollBack(self,fact_payment):
        self.bx_client.fact_payment.update(FactPayment(
            id=fact_payment.id,
            stage_id=fact_payment.previous_stage_id,
                )
            )


    def update(self,fact_payment,operation,payment_rule):
        self._updateFactPayment(fact_payment.id,operation,fact_payment.tm_payment_id)
        self._updatePaymentRule(payment_rule)