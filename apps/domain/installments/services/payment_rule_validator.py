from apps.integrations.bx24.lib.services.client import Bx24Client


class ValidationError(Exception):
    pass


class PaymentValidator:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client