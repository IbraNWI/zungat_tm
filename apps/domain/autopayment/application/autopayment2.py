from apps.integrations.bx24.lib.schemas.crm.smart_process.fact_payment import FactPayment

from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

from apps.domain.autopayment.services import (
    InstallmentLoader,DataNotFoundError,
    InstallmentValidator,ValidationError,
    InstallmentCalculation,CalculateError,
    MakeOperation,TMOperationError,
    CreatePayment,CreatePaymentError
)



class AutopaymentApplication:
    
    def __init__(self):
        self.bx_client = Bx24Client()
        self.tm_client = TMClient()
        self.installment_loader = InstallmentLoader(self.bx_client)
        self.installment_validator = InstallmentValidator(self.bx_client)
        self.installment_calculation = InstallmentCalculation(self.tm_client)
        self.installment_operation = MakeOperation(self.tm_client)
        self.installment_create_payment = CreatePayment(self.bx_client)
    

    def execute(self):
        print("Начало автосписания")
        installments = self.installment_loader.load()
        installments = self.installment_validator.validate(installments)
        print("Кол-во корректных платежей:",len(installments))
        installments = self.installment_calculation.calculate(installments)
        installments = self.installment_operation.make(self.installments)
        installments = self.installment_create_payment.create()
        print("Завершение работы")