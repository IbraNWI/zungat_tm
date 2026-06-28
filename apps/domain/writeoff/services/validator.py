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

    def _checkPayment(self,fact_payment,deal):

        if fact_payment.payment_type_id != 255: # Если тип платежа не подходит
            raise ValidationError("Некорректный тип платежа")

        if fact_payment.payment_state_id != 289: # Если платеж уже принят
            raise ValidationError("Платеж уже был обработан")
        
        
        if fact_payment.cenceled_tm_payment_id is not None: # Если платеж уже был отменен до этого
            raise ValidationError("Платеж уже был отменен в TM")

        check_sum = [
            deal.total_arest_sum,
            deal.installment_pay_sum,
            fact_payment.opportunity
            ]
        check_sum = [i for i in check_sum if i is not None]
        
        if sum(check_sum) > deal.opportunity: # Сумма платежа больше чем нужно для закрытия рассрочки
            raise ValidationError("Сумма платежа больше чем нужно для закрытия рассрочки")
   

    def validate(self,fact_payment,deal,payment_rule):
        # self._checkDeal(deal)
        self._checkPaymentRule(payment_rule)
        self._checkPayment(fact_payment,deal)