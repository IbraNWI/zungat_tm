import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zungat_tm.settings")
django.setup()

from apps.domain.autopayment.application.autopayment2 import (
    AutopaymentApplication
)
from apps.domain.depositarrest.application.depositarrest import DepositArrest




def check():
    from apps.integrations.bx24.lib.services.client import Bx24Client
    bx_client = Bx24Client()
    payment_rule = bx_client.payment_rule.get(717)
    print(payment_rule)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def main():
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


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def deposit_arrest_test():
    deposit_arrest = DepositArrest()
    deposit_arrest.execute()


if __name__ == "__main__":  
    deposit_arrest_test()
    # check()
