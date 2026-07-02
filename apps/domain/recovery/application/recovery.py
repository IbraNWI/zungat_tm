from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient

from apps.domain.recovery.services import DriverLoader


class AutopaymentApplication:
    
    def __init__(self):
        self.bx_client = Bx24Client()
        self.tm_client = TMClient()
        self.driver_loader = DriverLoader()
    

    def execute(self):
        ...