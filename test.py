import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zungat_tm.settings")  # <-- путь к твоим settings
django.setup()

from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.schemas import (
    Driver,Operation)
from apps.integrations.bx24.lib.schemas import PaymentRule

def request_test():
    bx_client = Bx24Client()

    rules = bx_client.payment_rule.list(filters={})
    for r in rules:
        print(bx_client.deal.get(entity_id=r.deal_id))

def get_factPayment():
    bx_client = Bx24Client()

    payments = bx_client.fact_payment.list(filters={})
    print(payments)

def fields_get():

    bx_client = Bx24Client()
    print(bx_client.fact_payment.fields())


def run_test():
    from apps.domain.autopayment.application.installments import AutopaymentApplication
    autopayment = AutopaymentApplication()
    autopayment.execute()

if __name__ == "__main__":
    fields_get()
