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

    def _checkPayment(self,fact_payment,deal,payment_rule):

        if fact_payment.is_accepted is True: # Если платеж уже применен
            raise ValidationError("Payment is accepted")
        
        if fact_payment.payment_type_id != 255: # Если тип платежа не подходит
            raise ValidationError("Payment type is incorrect")

        check_sum = [
            deal.total_arest_sum,
            deal.installment_pay_sum,
            fact_payment.opportunity
            ]
        check_sum = [i for i in check_sum if i is not None]
        
        if sum(check_sum) > deal.opportunity: # Сумма платежа больше чем нужно для закрытия рассрочки
            raise ValidationError("Payment has too high opportunity")
   

    def validate(self,fact_payment,deal,payment_rule):
        self._checkDeal(deal)
        self._checkPaymentRule(payment_rule)
        self._checkPayment(fact_payment,deal,payment_rule)