from apps.integrations.bx24.lib.services.client import Bx24Client

class DataNotFoundError(Exception):
    pass

class WriteoffDataLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client

    def load(self, fact_payment_id: int):
        fact_payment = self.bx_client.fact_payment.get(entity_id=fact_payment_id)

        if not fact_payment:
            raise DataNotFoundError("Фактический платеж не найден")

        if not fact_payment.deal_id:
            raise DataNotFoundError("У фактического платежа нет сделки")

        deal = self.bx_client.deal.get(entity_id=fact_payment.deal_id)

        if not deal:
            raise DataNotFoundError("Deal not found")

        if not deal.payment_rule:
            raise DataNotFoundError("В сделке отсутствует правило списаний")

        payment_rule = self.bx_client.payment_rule.get(entity_id=deal.payment_rule)

        if not payment_rule:
            raise DataNotFoundError("Правило списаний не найдено")

        return fact_payment, deal, payment_rule