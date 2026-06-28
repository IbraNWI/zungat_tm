from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.domain.autopayment.schemas.installment import Installment



class DataNotFoundError(Exception):
    pass



class InstallmentLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client

    def _loadPaymentRules(self):
        """Нужно запрашивать все ПС а не первые 50"""
        payment_rules = self.bx_client.payment_rule.iter_list(
            filters={}
            )
        return list(payment_rules)
    
    def _loadDeals(self,deal_ids):
        """Нужно разделить список на подсписки и запрашивать несколько раз"""
        deals = self.bx_client.deal.iter_list(filters={"id":deal_ids})
        
        return list(deals)
    
    def _makeInstallments(self,payment_rules,deals):
        """Создаем платежи. В случае, если в правиле списаний есть сделка,
           ее добавляем в платеж"""
        installments = []
        for payment_rule in payment_rules:
            installment = Installment(payment_rule=payment_rule)
            for deal in deals:
                if payment_rule.deal_id == deal.id:
                    installment.deal = deal
            installments.append(installment)
        
        return installments


    def load(self):
        payment_rules = self._loadPaymentRules()
        print("всего правил списаний:",len(payment_rules))
        deal_ids = [payment_rule.deal_id for payment_rule in payment_rules if payment_rule.deal_id is not None]
        print("всего id сделок в ПС:",len(deal_ids))
        deals = self._loadDeals(deal_ids)
        print("всего сделок получено:",len(deals))
        installments = self._makeInstallments(payment_rules,deals)
        return installments
