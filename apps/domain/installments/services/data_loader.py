from apps.integrations.bx24.lib.services.client import Bx24Client

class DataNotFoundError(Exception):
    pass


class InstallmentLoader:

    def __init__(self, bx_client: Bx24Client):
        self.bx_client = bx_client

    def load(self):
        payment_rules = self.bx_client.payment_rule.list(filters={
            "is_active":269,
            ">=first_pay_date":"30.06.2026"
            }
        )
        [print(i.id,i.first_pay_date) for i in payment_rules]