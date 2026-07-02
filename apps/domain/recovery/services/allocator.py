from datetime import datetime,timezone

from apps.domain.recovery.models import DriverSyncState
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.domain.recovery.schemas.driver import Driver,Installment
from apps.integrations.tm_driver.lib.schemas import Operation
from apps.integrations.bx24.lib.schemas import FactPayment



class OperationAllocation:
    def __init__(self,tm_client:TMClient):
                self.tm_client = tm_client
    
    def _checkAccessOperation(self,operation:Operation) -> bool:
        driver_sync_state = DriverSyncState.objects.filter(driver_id=operation.driver_id).first()
        if driver_sync_state is None:
            return True
        else:
            if driver_sync_state.last_processed_operation_id >= operation.id:
                return False
        return True

    def _checkOperation(self,operation:Operation):
        if operation.oper_type != "receipt":
            return False
        if not self._checkAccessOperation(operation):
            return False
        if operation.cancelled_oper_id != 0:
            return False
        if operation.cancelled_by_oper_id != 0:
            return False
        # if "отмена" in operation.title.lower():
        #     return False
        
        return True

    def _getCorrectOperations(self,driver:Driver) -> list[Operation]:
        correct_operations = []
        for operation in driver.operations:
            if self._checkOperation(operation):
                correct_operations.append(operation)

        return correct_operations

    def _getOldestArestedDate(self,installments:list[Installment]) -> datetime:
        start_time = datetime.now(timezone.utc)
        for installment in installments:
            arested_date = installment.payment_rule.arested_date
            if arested_date is not None:
                arested_date = datetime.fromisoformat(arested_date)
            else:
                arested_date = start_time

            if arested_date < start_time:
                start_time = arested_date
        return start_time
 
    def loadReceiptes(self,driver:Driver) -> list[Operation]:
        start_time = self._getOldestArestedDate(driver.installments)
        finish_time = datetime.now(timezone.utc)
        operations = self.tm_client.operation.get(
            driver_id=driver.driver_id,
            start_time=start_time,
            finish_time=finish_time
            )
        driver.operations = operations
        print("Всего операций запрошено:",len(operations))
        operations = self._getCorrectOperations(driver)
        print("Всего корректных операций:",len(operations))
        return operations
    


class InstallmentAllocation:
    def __init__(self):
        ...
    
    def _getOperationsSum(self,operations:list[Operation]) -> float:
        operations_sum = 0
        for operation in operations:
            operations_sum += operation.sum
        return operations_sum
    
    def _makePayment(self,installment:Installment,arest_sum:float) -> FactPayment:
        return FactPayment(
            title=f"Списание ареста. Зунгат-Тешам",
            deal_id=installment.deal.id,
            category_id=15,
            stage_id="DT1052_15:SUCCESS",
            opportunity=arest_sum,
            company_id=installment.deal.company_id,
            contact_ids=installment.deal.contact_ids,
            assigned_by_id=1,
            created_by_id=1,
            payment_type_id=251,
            tm_payment_id=0,
        )
    
    def allocate(self, driver: Driver) -> list[Installment]:
        operations_sum = self._getOperationsSum(driver.operations)
        for installment in driver.installments:
            if operations_sum <= 0:
                break
            arest_sum = installment.deal.total_arest_sum
            payment_sum = min(operations_sum, arest_sum)
            installment.fact_payment = self._makePayment(
                installment=installment,
                arest_sum=payment_sum
            )
            operations_sum -= payment_sum
        return driver.installments

class DriverAllocation:
    def __init__(self,tm_client:TMClient):
        self.operation_allocation = OperationAllocation(tm_client)
        self.installment_allocation = InstallmentAllocation()
    
    
    def allocate(self,drivers:list[Driver]):
        for driver in drivers:
            driver.operations = self.operation_allocation.loadReceiptes(driver)
            driver.installments = self.installment_allocation.allocate(driver)
        return drivers