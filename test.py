import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zungat_tm.settings")  # <-- путь к твоим settings
django.setup()

from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.schemas import (
    Driver,Operation)
from apps.integrations.bx24.lib.schemas import PaymentRule

from apps.domain.installments.application.installments import InstallmentService


InstallmentService().execute()