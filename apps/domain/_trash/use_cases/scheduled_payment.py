from apps.integrations.bx24.lib.services.client import Bx24Client

from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient


def checkOperation():
    ...


def main():
    bx_client = Bx24Client()
    tm_client = TaxiMasterClient()
    
    payment_rules = bx_client.payment_rule.list(
        filters={"ufCrm15RuleActivity":257})
    
    for rule in payment_rules:
        driver = tm_client.driver.get(id=rule.driver_id)
