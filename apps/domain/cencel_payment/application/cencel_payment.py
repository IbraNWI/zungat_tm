from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

from apps.domain.cencel_payment.services import (
    CencelPaymentLoader,DataNotFoundError,
    PaymentValidator,ValidationError,
    PaymentCalculation,CalculateError,
    MakeOperation,TMOperationError,
    UpdatePayment,UpdatePaymentError
)



class CencelPaymentService:
    
    def __init__(self):
        self.bx_client = Bx24Client()
        self.tm_client = TMClient()

        self.cencel_payment_loader = CencelPaymentLoader(self.bx_client)
        self.payment_validator = PaymentValidator(self.bx_client)
        self.payment_calculation = PaymentCalculation(self.tm_client)
        self.make_operation = MakeOperation(self.tm_client)
        self.update_payment = UpdatePayment(self.bx_client)
    
    def _addError(self, text: str, id:int):
        self.bx_client.fact_payment.timeline.add(
            TimelineMessage(
                entity_id=id,
                title="Ошибка списания денег",
                text=text,
                icon_code="circle-crossed"
            )
        )

    def _addEvent(self,place:str,id:int):
        if place == "start":
            message = TimelineMessage(
                entity_id=id,
                title="Обработка платежа",
                text="Обработка платежа",
                icon_code="check"
                )
        elif place == "finish":
            message = TimelineMessage(
                entity_id=id,
                title="Платеж отменен",
                text="Успешный платеж",
                icon_code="complete"
                )
        self.bx_client.fact_payment.timeline.add(message)



    def execute(self,fact_payment_id):
        self._addEvent(place="start",id=fact_payment_id)
        try:
            fact_payment = self.cencel_payment_loader._loadPayment(fact_payment_id)
        except DataNotFoundError as e:
            self._addError(text=str(e),id=fact_payment_id)
            return

        try:
            deal = self.cencel_payment_loader._loadDeal(fact_payment.deal)
            payment_rule = self.cencel_payment_loader._loadPaymentRule(deal.payment_rule)
        except DataNotFoundError as e:
            self._addError(text=str(e),id=fact_payment_id)
            self.update_payment.updateRollBack(fact_payment)
            return
        
        try:
            self.payment_validator.validate(fact_payment,deal,payment_rule)
        except ValidationError as e:
            self._addError(text=str(e),id=fact_payment_id)
            self.update_payment.updateRollBack(fact_payment)
            return
        
        # try:
        #     paid,arrest = self.payment_calculation.calculate(fact_payment,payment_rule)
        # except CalculateError as e:
        #     self._addError(text=str(e),id=fact_payment_id)
        #     return
        
        # try:
        #     operation = self.make_operation.make(fact_payment,payment_rule)
        # except TMOperationError as e:
        #     self._addError(text=str(e),id=fact_payment_id)
        #     return
        
        # try:
        #     self.update_payment.update(fact_payment,operation,payment_rule,paid,arrest)
        # except UnicodeDecodeError as e:
        #     self._addError(text=str(e),id=fact_payment_id)
        #     return
 
        # self._addEvent(place="finish",id=fact_payment_id)