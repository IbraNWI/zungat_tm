from apps.integrations.bx24.lib.services.client import Bx24Client

class DataNotFoundError(Exception):
    pass


class CencelPaymentLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client
    
    def _loadPayment(self,fact_payment_id:int):
        fact_payment = self.bx_client.fact_payment.get(entity_id=fact_payment_id)
        if not fact_payment:
            raise DataNotFoundError("Фактический платеж не был найден")
        return fact_payment
    
    def _loadDeal(self,deal_id):
        if not deal_id:
            raise DataNotFoundError("Нет рассрочки по данному фактическому платежу")
        deal = self.bx_client.deal.get(entity_id=deal_id)
        if not deal:
            raise DataNotFoundError("Нет рассрочки по данному фактическому платежу")
        return deal
    
    def _loadPaymentRule(self,payment_rule_id):
        if not payment_rule_id:
            raise DataNotFoundError("Рассрочка не имеет правила списаний")
        payment_rule = self.bx_client.payment_rule.get(entity_id=payment_rule_id)
        if not payment_rule:
            raise DataNotFoundError("Рассрочка не имеет правила списаний")
        return payment_rule

    def load(self, fact_payment_id: int):
        fact_payment = self._loadPayment(fact_payment_id)
        deal = self._loadDeal(fact_payment.deal_id)
        payment_rule = self._loadPaymentRule(deal.payment_rule)


        return fact_payment, deal, payment_rule