from apps.integrations.bx24.lib.services.client import Bx24Client

from apps.domain.recovery.schemas.driver import Driver, Installment
from apps.integrations.bx24.lib.schemas import Deal,PaymentRule



class DataNotFoundError(Exception):
    pass


class DriverLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client
    
    def _loadPaymentRules(self) -> list[PaymentRule]:
        payment_rules = self.bx_client.payment_rule.iter_list(
            filters={"@is_active":[271]}
            )
        return list(payment_rules)
    
    def _loadDeals(self,deal_ids) -> list[Deal]:
        deals = self.bx_client.deal.iter_list(filters={"id":deal_ids})
        return list(deals)
    
    def _makeDrivers(self,payment_rules,deals) -> list[Driver]:
        deals_by_id = {deal.id: deal for deal in deals}

        # Временное хранилище водителей
        drivers_dict = {}

        for payment_rule in payment_rules:
            driver_id = payment_rule.driver_id

            # создаем водителя при необходимости
            if driver_id not in drivers_dict:
                drivers_dict[driver_id] = Driver(
                    driver_id=driver_id,
                    installments=[],
                    operations=[],
                )

            installment = Installment(
                payment_rule=payment_rule,
                deal=deals_by_id.get(payment_rule.deal_id),
            )

            drivers_dict[driver_id].installments.append(installment)

        # Готовый список
        drivers = list(drivers_dict.values())

            

        return drivers
    
    def load(self) -> list[Driver]:
        payment_rules = self._loadPaymentRules()
        deal_ids = [payment_rule.deal_id for payment_rule in payment_rules if payment_rule.deal_id is not None]
        deals = self._loadDeals(deal_ids)
        drivers = self._makeDrivers(payment_rules,deals)
        return drivers
