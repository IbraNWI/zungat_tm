import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zungat_tm.settings")  # <-- путь к твоим settings
django.setup()

from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.bx24.lib.schemas.crm.smart_process.fact_payment import FactPayment
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

# from bx24.integration.code.update_contact_info import main as update_contact
# tm_client = TaxiMasterClient()
bx_client = Bx24Client()

# print(tm_client.driver.list())

fields = bx_client.payment_rule.list(filters={"payment_frequency":175})
print(fields)