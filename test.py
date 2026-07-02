import os
from datetime import datetime, timezone
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zungat_tm.settings")
django.setup()

from apps.domain.autopayment.application.autopayment2 import (
    AutopaymentApplication
)
from apps.domain.depositarrest.application.depositarrest import DepositArrest

from apps.domain.depositarrest.models import ArrestedDeposit




def check():
    from apps.integrations.bx24.lib.services.client import Bx24Client
    bx_client = Bx24Client()
    payment_rule = bx_client.fact_payment.fields()
    print(payment_rule)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                       AUTOPAYMENTS                           #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def test_autopayment():
    from datetime import datetime,timezone
    from apps.integrations.bx24.lib.services.client import Bx24Client
    from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient
    from apps.domain.autopayment.services import (
        InstallmentLoader, InstallmentValidator,
        InstallmentCalculation, MakeOperation, CreatePayment
    )

    installments = InstallmentLoader(Bx24Client()).load()
    installments = InstallmentValidator(Bx24Client()).validate(installments)
    print("Корректных платежей:",len(installments))
    installments = InstallmentCalculation(TaxiMasterClient()).calculate(installments)
    # installments = MakeOperation(TaxiMasterClient()).make(installments)
    # installments = CreatePayment(Bx24Client()).create(installments)

    for installment in installments:
        print(f"{installment.payment_rule.id} | {installment.operation.oper_sum} | {installment.fact_payment.opportunity} - {installment.fact_payment.arest_sum}")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                       RECOVERY                               #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_recovery():
    from apps.integrations.bx24.lib.services.client import Bx24Client
    from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient
    from apps.domain.recovery.services import (
        DriverAllocation,DriverLoader,DriverValidator,CreatePayment
    )
    drivers = DriverLoader(Bx24Client()).load()
    drivers = DriverValidator().validate(drivers)
    drivers = DriverAllocation(TaxiMasterClient()).allocate(drivers)
    drivers = CreatePayment(Bx24Client()).create(drivers)




    # drivers = DriverAllocation(TaxiMasterClient()).allocate(drivers)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == "__main__": 
    # check()
    test_recovery()
    # test_autopayment()

