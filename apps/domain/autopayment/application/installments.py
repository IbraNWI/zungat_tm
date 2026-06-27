from apps.integrations.bx24.lib.schemas.crm.smart_process.fact_payment import FactPayment
from datetime import date, datetime, timezone

from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.bx24.lib.schemas.crm.timeline_message import TimelineMessage

from apps.domain.autopayment.services import (
    InstallmentLoader,DataNotFoundError
)



class AutopaymentApplication:
    
    def __init__(self):
        self.bx_client = Bx24Client()
        self.tm_client = TMClient()

        #self.installment_loader = InstallmentLoader(self.bx_client)

    def is_valid_transaction(self):
        return False

    def _is_fully_paid(self,installment_amout, payed_amount) -> bool:
        if payed_amount < installment_amout:
            return False
        else:
            return True
    
    def _is_payment_due(self, last_payment_date, payment_frequency) -> bool:

        today = date.today()
        if payment_frequency == 171: #daily
            payment_frequency = 1 
        elif payment_frequency == 173: #weekly
            payment_frequency = 7
        elif payment_frequency == 175: #monthly
            payment_frequency = 30
        else:
            print(f"unexpected frequency value {payment_frequency} aborting" )
            raise ValueError
        if today - last_payment_date >= payment_frequency:
            return True
        else:
            return False


    def create_reccurent_payment(self,deal,payment_rule) -> FactPayment:
        tz = timezone.utc
        creation_date = str(datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"))
        title = f"Автоматическое списание. Зунгат-Тешам от {creation_date}"
        company_id = payment_rule.company_id
        contact_id = payment_rule.contact_id
        contact_ids = payment_rule.contact_ids
        category_id = payment_rule.category_id
        stage_id = "ASDASDJSADJSADSAD"
        
        payment = FactPayment(

        )


    def get_active_payment_rules(self):
        return self.bx_client.payment_rule.list(filters={"is_active" : 1})

    def get_deal(self, deal_id: int):
        return self.bx_client.payment_rule.get(entity_id=deal_id)

    def execute(self) -> None:
        
        payment_rules = self.get_active_payment_rules()


        for payment_rule in payment_rules: 
            deal = self.get_deal(payment_rule.deal_id) 

            recurring_amount = payment_rule.payment_sum
            installment_amount = deal.opportunity
            payed_amount = deal.installment_pay_sum
            remaining_amount = installment_amount - payed_amount
            last_payment_date = payment_rule.last_payment_date
            payment_frequency = payment_rule.payment_frequency

            if self._is_fully_paid(installment_amount, payed_amount):
               return None 

            if not self._is_payment_due(last_payment_date, payment_frequency):
                return None
            
            payment_amount = recurring_amount
            if payment_amount > remaining_amount:
                payment_amount = remaining_amount

            new_payment = self.create_reccurent_payment(deal,payment_rule)


            
            if self.is_valid_transaction():
                self.bx_client.fact_payment.add(new_payment)
        
        
