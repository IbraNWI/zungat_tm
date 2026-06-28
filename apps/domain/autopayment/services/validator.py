from datetime import datetime,timedelta,timezone
from dateutil.relativedelta import relativedelta
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.domain.autopayment.schemas.installment import Installment
from apps.integrations.bx24.lib.schemas import Deal,PaymentRule

class ValidationError(Exception):
    pass


class PaymentRuleValidate:
    def __init__(self):
        ...

    def checkPaymentDate(self, payment_rule: PaymentRule) -> bool:
        today = datetime.now(timezone.utc).date()

        first_pay_date = datetime.fromisoformat(payment_rule.first_pay_date).date()

        if first_pay_date > today:
            return False

        last_payment_date = (
            datetime.fromisoformat(payment_rule.last_payment_date).date()
            if payment_rule.last_payment_date
            else None
        )

        frequency = payment_rule.payment_frequency
        last_expected = first_pay_date
        n = 1

        while True:
            if frequency == 171:
                next_date = first_pay_date + timedelta(days=n)
            elif frequency == 173:
                next_date = first_pay_date + timedelta(weeks=n)
            elif frequency == 175:
                next_date = first_pay_date + relativedelta(months=n)
            else:
                return False

            if next_date > today:
                break

            last_expected = next_date
            n += 1

        if last_payment_date is None:
            return True

        return last_payment_date < last_expected



    def checkIsActive(self,payment_rule:PaymentRule) -> bool:
        if payment_rule.is_active != 269:
            return False
        
        return True

    def hasDriverId(self,payment_rule:PaymentRule) -> bool:
        if  payment_rule.driver_id is None:
            return False
        
        return True


class DealValidate:
    def __init__(self):
        ...
    
    def checkPaymentSum(self,deal:Deal):
        opportunity = deal.opportunity if deal.opportunity is not None else 0
        total_arest_sum = deal.total_arest_sum if deal.total_arest_sum is not None else 0
        installment_pay_sum = deal.installment_pay_sum if deal.installment_pay_sum is not None else 0

        if (total_arest_sum + installment_pay_sum) >= opportunity:
            # По рассрочке уже списаны все деньги
            return False
        
        return True


class InstallmentValidator:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client
        self.payment_rule_validate = PaymentRuleValidate()
        self.deal_validate = DealValidate()

    
    def _validatePaymentRule(self,payment_rule:PaymentRule) -> bool:

        if not self.payment_rule_validate.checkPaymentDate(payment_rule):
            # Проверка возможности списания по дате
            return False
        if not self.payment_rule_validate.checkIsActive(payment_rule):
            # Если ПС не активно
            return False
        if not self.payment_rule_validate.hasDriverId(payment_rule):
            # Если в ПС нет id водителя
            return False
        
        return True
    

    def _validateDeal(self,deal:Deal) -> bool:
        if deal is None:
            return False
        
        if not self.deal_validate.checkPaymentSum(deal):
            return False
        
        return True

    
    def validate(self, installments: list[Installment]) -> list[Installment]:
        """Проход по всем платежам. Проверка корректности для списания"""
        valid_installments = []

        for installment in installments:
            if not self._validateDeal(installment.deal):
                # если платеж не проходит валидацию по сделке, то платеж пропускается
                continue

            if not self._validatePaymentRule(installment.payment_rule):
                # если платеж не проходит валидацию по Пс, то платеж пропускается
                continue

            valid_installments.append(installment)

        return valid_installments