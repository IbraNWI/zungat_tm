from apps.integrations.bx24.lib.services.client import Bx24Client


class ValidationError(Exception):
    pass


class PaymentValidator:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client
    
    def _checkDeal(self,deal):
        
        if deal.category_id not in [19]: # Если сделка по платежу не нужной воронке
            raise ValidationError("Рассрочка по платежу находится на неподходящей воронке")

    def _checkPaymentRule(self,payment_rule):        
        if payment_rule.driver_id is None:
            raise ValidationError("В правиле списаний не указан позывной водителя")

    def _checkPayment(self,fact_payment):
        if fact_payment.payment_state_id != 285: # Если платеж не был отменен
            raise ValidationError("Платеж не был до этого принят")
    
    
    
    def validate(self,fact_payment,deal,payment_rule):
        self._checkDeal(deal)
        self._checkPaymentRule(payment_rule)
        self._checkPayment(fact_payment)