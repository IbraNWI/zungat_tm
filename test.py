import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zungat_tm.settings")  # <-- путь к твоим settings
django.setup()

from tm_driver.lib.services.client import TaxiMasterClient


tm_client = TaxiMasterClient()

print(tm_client.driver.list())
