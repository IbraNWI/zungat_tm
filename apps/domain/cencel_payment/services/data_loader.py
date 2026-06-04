from apps.integrations.bx24.lib.services.client import Bx24Client

class DataNotFoundError(Exception):
    pass


class CencelPaymentLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client

    def load(self, fact_payment_id: int):
        raise DataNotFoundError("Method does not work")
    
    
        fact_payment = self.bx_client.fact_payment.get(entity_id=fact_payment_id)

        if not fact_payment:
            raise DataNotFoundError("Fact payment not found")

        if not fact_payment.deal_id:
            raise DataNotFoundError("Fact payment has no deal")

        deal = self.bx_client.deal.get(entity_id=fact_payment.deal_id)

        if not deal:
            raise DataNotFoundError("Deal not found")

        if not deal.payment_rule:
            raise DataNotFoundError("Deal has no payment rule")

        payment_rule = self.bx_client.payment_rule.get(entity_id=deal.payment_rule)

        if not payment_rule:
            raise DataNotFoundError("Payment rule not found")

        return fact_payment, deal, payment_rule