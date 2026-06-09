from apps.integrations.bx24.lib.services.client import Bx24Client

class DataNotFoundError(Exception):
    pass


class RecoveryPaymentRules:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client
    

    def _loadPaymentRules(self):
        payment_rules = self.bx_client.payment_rule.iter_list(
            filters={}
            )
        
        return payment_rules
    