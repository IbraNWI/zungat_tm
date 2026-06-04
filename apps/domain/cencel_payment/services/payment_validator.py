from apps.integrations.bx24.lib.services.client import Bx24Client


class ValidationError(Exception):
    pass


class PaymentValidator:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client
    
    def _checkDeal(self,deal):
        
        if deal.category_id not in [19]: # Если сделка по платежу не нужной воронке
            raise ValidationError("Payment's deal is on wrong category")

    def _checkPaymentRule(self,payment_rule):        
        if payment_rule.driver_id is None:
            raise ValidationError("Payment rule has no driver_id")

    def _checkPayment(self,fact_payment):
        if fact_payment.is_accepted is not True: # Если платеж не был принят
            raise ValidationError("Payment was not accepted")
    
    
    
    def validate(self,fact_payment,deal,payment_rule):
        self._checkDeal(deal)
        self._checkPaymentRule(payment_rule)
        self._checkPayment(fact_payment)