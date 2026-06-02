from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient

def main(contact_id:int):
    tm_client = TaxiMasterClient()
    bx_client = Bx24Client()

    contact = bx_client.contact.get(entity_id=contact_id)
    if contact.driver_id is None:
        return None
    driver = tm_client.driver.get(id=contact.driver_id)
    contact.balance = driver.balance
    contact = bx_client.contact.update(contact)

    