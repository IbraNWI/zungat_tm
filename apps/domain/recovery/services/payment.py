from datetime import datetime

from apps.domain.recovery.models import DriverSyncState
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.domain.recovery.schemas.driver import Driver,Installment
from apps.integrations.bx24.lib.schemas import FactPayment



class CreatePayment:
    def __init__(self,bx_client:Bx24Client):
        self.bx_client = bx_client


    def _getLastOperationId(self,driver:Driver) -> int:
        last_operation_id = 0
        for operation in driver.operations:
            if operation.id > last_operation_id:
                last_operation_id = operation.id
        
        return last_operation_id
    
    def _updateDriverSyncState(self,driver:Driver):
        operation_id = self._getLastOperationId(driver)
        DriverSyncState.objects.update_or_create(
            driver_id=driver.driver_id,
            last_processed_operation_id=operation_id
        )

    def _createFactPayment(self,fact_payment:FactPayment):
        try:
            self.bx_client.fact_payment.add(fact_payment)
        except:
            # Не получилось создать платеж
            print("Возникла ошибка с созданием платежа")
            
    def _getPaymentList(self,installments:list[Installment]) -> list[FactPayment]:
        payment_list = []
        for installment in installments:
            if installment.fact_payment is not None:
                payment_list.append(installment.fact_payment)
        
        return payment_list

    def create(self,drivers:list[Driver]):
        for driver in drivers:
            payment_list = self._getPaymentList(driver.installments)
            # for payment in payment_list:
            #     self._createFactPayment(payment)
            # self._updateDriverSyncState(driver)
            
