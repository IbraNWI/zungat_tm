"""
Скрипт для ручныхсписаний.
При создании факт. платежа на стороне битрикса отправляется запрос
на интгерацию. Происходит проверка сделки по рассрочке  у  платежа
После уже проверка правила списания у рассрочки. В случае  наличия
правила списания, проверяется его активность. При  таких  условиях
происходит списание ТМ по факт. платежу
"""

from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.bx24.lib.schemas.crm.smart_process.fact_payment import FactPayment
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient
from apps.integrations.tm_driver.lib.schemas.operation import Operation



class PaymentError(Exception):
    """Базовая ошибка списания"""


class DealNotAttachedError(PaymentError):
    pass


class PaymentRuleNotFoundError(PaymentError):
    pass


class PaymentRuleInactiveError(PaymentError):
    pass


def add_error_timeline(
        bx_client: Bx24Client,
        fact_payment_id: int,
        text: str):
    message = TimelineMessage(
        entity_id=fact_payment_id,
        title="Ошибка списания",
        text=text,
        icon_code="cross-air")
    
    bx_client.fact_payment.timeline.add(message)
    bx_client.fact_payment.update(FactPayment(
        id=fact_payment_id,stage_id="DT1052_15:FAIL"))


def get_payment_rule(bx_client: Bx24Client,deal_id: int):
    rules = bx_client.payment_rule.list(filters={"parentId2": deal_id})
    if not rules:
        raise PaymentRuleNotFoundError("У рассрочки факт. платежа нет правила списания")
    rule = rules[0]

    if rule.is_active != 257:
        raise PaymentRuleInactiveError("Правило списаний по рассрочке не активно")
    return rule


def validate_fact_payment(bx_client: Bx24Client,fact_payment):
    if fact_payment.deal_id is None:
        raise DealNotAttachedError("За факт. платежом не закреплена сделка по рассрочке")

    return get_payment_rule(bx_client=bx_client,deal_id=fact_payment.deal_id)


def process_payment(
        bx_client:Bx24Client,
        tm_client: TaxiMasterClient,
        fact_payment,
        payment_rule):
    
    operation = Operation(
        driver_id=payment_rule.driver_id,
        oper_sum=fact_payment.opportunity,
        name="Название",
        comment="Описнаие",
        oper_type="expense"
        )
    
    operation = tm_client.operation.add(operation)
    fact_payment.tm_payment_id = operation.id
    fact_payment.stage_id = "DT1052_15:SUCCESS"
    fact_payment = bx_client.fact_payment.update(fact_payment)


def main(fact_payment_id: int) -> bool:
    tm_client = TaxiMasterClient()
    bx_client = Bx24Client()

    fact_payment = bx_client.fact_payment.get(entity_id=fact_payment_id)

    try:
        payment_rule = validate_fact_payment(bx_client=bx_client,fact_payment=fact_payment)

        process_payment(tm_client=tm_client,fact_payment=fact_payment,payment_rule=payment_rule)

        return True

    except PaymentError as e:
        add_error_timeline(bx_client=bx_client,fact_payment_id=fact_payment.id,text=str(e))
        return False

    except Exception:
        add_error_timeline(
            bx_client=bx_client,
            fact_payment_id=fact_payment.id,
            text="Возникла проблема на стороне интеграции")
        return False
    


    
    