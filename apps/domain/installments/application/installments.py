from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

from apps.domain.installments.services import (
    InstallmentLoader,DataNotFoundError
)



class InstallmentService:
    
    def __init__(self):
        self.bx_client = Bx24Client()
        self.tm_client = TMClient()

        self.installment_loader = InstallmentLoader(self.bx_client)


    def execute(self):
        self.installment_loader.load()