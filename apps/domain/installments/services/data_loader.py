from datetime import datetime
from apps.integrations.bx24.lib.services.client import Bx24Client

class DataNotFoundError(Exception):
    pass




class InstallmentLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client

    def _loadPaymentRules(self):
        payment_rules = self.bx_client.payment_rule.list(
            filters={}
            )
        return payment_rules

    def _loadDeals(self,deals_ids:list):
        deals_list = []
        for deal_id in deals_ids:
            deal = self.bx_client.deal.get(entity_id=deal_id)
            if deal is not None:
                deals_list.append(deal)
        
        return deals_list

    def load(self):
        payment_rules = self._loadPaymentRules()        