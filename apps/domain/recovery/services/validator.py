
from apps.domain.recovery.schemas.driver import Driver,Installment
from apps.integrations.bx24.lib.schemas import Deal,PaymentRule


class InstallmentValidator:
    def __init__(self):
        ...

    def _checkPaymentRule(self,payment_rule:PaymentRule) -> bool:
        if payment_rule is None:
            return False
        if payment_rule.is_active not in [269,271]:
            return False
        
        return True

    def _checkDeal(self,deal:Deal) -> bool:
        if deal is None:
            return False
        
        total_arest_sum = deal.total_arest_sum if deal.total_arest_sum is not None else 0
        if total_arest_sum > 0:
            # проверка на наличие ареста в сделке
            return True
        else:
            return False
    
    def validInstallments(self,installments:list[Installment]):
        valid_installments = []
        for installment in installments:
            if not self._checkDeal(installment.deal):
                continue
            if not self._checkPaymentRule(installment.payment_rule):
                continue
            else:
                valid_installments.append(installment)
        return valid_installments

    
class DriverValidator:
    def __init__(self):
        self._deal_validator = InstallmentValidator()
    
    
    def validate(self, drivers:list[Driver]) -> list[Driver]:
        valid_drivers = []
        for driver in drivers:
            driver.installments = self._deal_validator.validInstallments(driver.installments)
            if len(driver.installments) > 0:
                # если у водителя есть рассрочки с арестом
                valid_drivers.append(driver)    
        return valid_drivers