from apps.domain.depositarrest.models import ArrestedDeposit
from apps.integrations.bx24.lib.services.client import Bx24Client
from apps.integrations.tm_driver.lib.schemas.operation import Operation
from apps.integrations.tm_driver.lib.services.client import TaxiMasterClient as TMClient
from apps.integrations.bx24.lib.schemas.crm.deal import Deal
from apps.integrations.bx24.lib.schemas.crm.smart_process.fact_payment import FactPayment
from apps.integrations.bx24.lib.schemas.crm.smart_process.payment_rule import PaymentRule
from apps.domain.autopayment.services import CreatePayment, CreatePaymentError
from datetime import datetime,timezone


INDEV = True



class DepositArrest:
    
    def __init__(self):
        self.bx_client = Bx24Client() 
        self.tm_client = TMClient()

    def get_deals(self) -> list[Deal]: 
        deals = self.bx_client.deal.iter_list(
            filters={"!total_arest_sum" : None}
        )
        return list(deals)

    def filter_deals_with_arrest(self, deals: list[Deal]) -> list[Deal]:
        #DEBUG
        for deal in deals:
            print(f'filter deal arrest sum is {deal}')
        deals_with_arrest = [deal for deal in deals if deal.total_arest_sum != None]
        print(deals_with_arrest)
        return [deal for deal in deals_with_arrest if deal.total_arest_sum > 0]

    def get_deal_last_payment_date(self, deal : Deal) -> FactPayment | None:
        payment_rule_id = deal.payment_rule
        if payment_rule_id != None:
            payment_rule = self.bx_client.payment_rule.get(payment_rule_id)
            if payment_rule != None:
                last_payment_date = payment_rule.last_payment_date
                return last_payment_date

        print(f'unable to find last payment date, no payment_rule_id in deal: {deal}')


    def get_driver_deposits_after(self,driver_id : int, last_payment_date) -> list[Operation]:
        
        finish_time = datetime.now(timezone.utc).date()

        last_payment_date = datetime.fromisoformat(last_payment_date).date()
        operations = self.tm_client.operation.get(
            driver_id=driver_id,
            start_time=last_payment_date,
            finish_time=finish_time
        )

        receipt_operations = [ oper for oper in operations if oper.oper_type == "receipt"]
        
        return receipt_operations

    def get_deal_driver_id(self, deal : Deal) -> int | None:
        payment_rule_id = deal.payment_rule
        if payment_rule_id != None:
            payment_rule = self.bx_client.payment_rule.get(payment_rule_id)
            if payment_rule != None:
                driver_id = payment_rule.driver_id
                if driver_id != None:
                    return driver_id
            else: 
                print(f'uable to get driver id from deal, {payment_rule} driver_id is None')
        else:
            print(f'unable to get driver id from deal, {deal} payment rule id is None')

    def get_arrested_deposits_after(self,driver_id : int, last_payment_date) -> list[ArrestedDeposit]:
        driver_arrested_deposits = ArrestedDeposit.objects.filter(driver_id=driver_id,deposit_date__gt=last_payment_date)
        return driver_arrested_deposits

    def create_new_arrested_deposit(self, deposit_operation : Operation) -> ArrestedDeposit:
        arrested_deposit = ArrestedDeposit(
            operation_id=deposit_operation.id,
            available_funds=deposit_operation.sum
        )
        return arrested_deposit

    def get_available_deposits_to_payment(self, deposits_operations, arrested_deposits, deal_arrest_amount) -> list[ArrestedDeposit]:
        deposits_available_funds = 0
        available_deposits = []
        
        for arrested_deposit in arrested_deposits:
            if arrested_deposit.is_fully_spent(): 
                continue
            else:
                deposits_available_funds += arrested_deposit.available_funds
                available_deposits.append(arrested_deposit)
            
            if deposits_available_funds >= deal_arrest_amount:
                return available_deposits
        
        arrested_deposits_ids = [ad.id for ad in arrested_deposits]
        for deposit_operation in deposits_operations:
            if deposit_operation.id in arrested_deposits_ids:
                continue
            else:
                new_arrested_deposit = self.create_new_arrested_deposit(deposit_operation)
                new_arrested_deposit.save()
                arrested_deposits_ids.append(new_arrested_deposit.operation_id)
                deposits_available_funds += new_arrested_deposit.available_funds
                available_deposits.append(new_arrested_deposit)

            if deposits_available_funds >= deal_arrest_amount:
                return available_deposits

        return available_deposits

    def create_fact_payment(self, deal : Deal, payment_amount : float, title=None) -> FactPayment | None:
        if payment_amount <= 0:
            print('payment_amount is 0, fact_payment creation abort')
            return None

        creation_time = datetime.now()
        success_stage_id="DT1052_15:SUCCESS"
        payment = FactPayment(
            title=title,
            created_time=creation_time,
            company_id=deal.compamy_id,
            contact_id=deal.contact_id,
            contacts_ids=deal.contacts_ids,
            category_id=deal.caterogy_id,
            stage_id=success_stage_id,
            assigned_by_id=deal.assigned_by_id,
            opportunity=payment_amount,
            deal_id=deal.id
        )
        return payment

    def process_deposits_to_pay_deal_arrest(self,deal_with_arrest : Deal):
        """
        Ищу дату последнего fact payment по deal в payment rule, 
        Но я не уверен что дата последнего fact payment всегда хранится там, 
        что если платеж был совершен без payment rule? такое вообще возможно?
        """
        print('starting to precess!')

        last_payment_date = self.get_deal_last_payment_date(deal_with_arrest)
        driver_id = self.get_deal_driver_id(deal_with_arrest)
        deal_arrest_amount = deal_with_arrest.total_arest_sum
        if last_payment_date == None:
            return None
        if driver_id == None:
            return None

        new_deposits = self.get_driver_deposits_after(driver_id,last_payment_date)
        arrested_deposits = self.get_arrested_deposits_after(driver_id,last_payment_date)

        available_deposits_to_payment = self.get_available_deposits_to_payment(new_deposits, arrested_deposits, deal_arrest_amount)

        arested_deposits_available_funds = 0
        used_deposits = []

        for deposit in available_deposits_to_payment:
            arested_deposits_available_funds += deposit.available_funds
            used_deposits.append(deposit)
            if arested_deposits_available_funds >= deal_arrest_amount:
                remaining_funds = arested_deposits_available_funds - deal_arrest_amount
                if remaining_funds < deposit.available_funds:
                    deposit = remaining_funds   ## SETTER FOR PROTECTION
                break
            else:
                deposit.available_funds = 0 ## SETTER FOR PROTECTION TODO

        if arested_deposits_available_funds <= 0:
            print('no available funds to pay arrest')
            return None

        
        payment_amount = arested_deposits_available_funds
        payment_title = f"Закрытие ареста сделки {deal_with_arrest.id} на сумму {payment_amount}"
        new_payment = self.create_fact_payment(deal_with_arrest,payment_amount,payment_title)
        if new_payment != None:

            if INDEV:
                print(f"new payment is {new_payment}")
            else:
                for deposit in used_deposits: # saving changes
                    deposit.save()
                self.bx_client.fact_payment.add(new_payment)


    def execute(self):

        print('getting deals')
        all_deals = self.get_deals()
        print('getting deals with arrest')
        deals_with_arrest = self.filter_deals_with_arrest(all_deals)

        for deal in deals_with_arrest:
            print(f'proccessing deal {deal}')
            self.process_deposits_to_pay_deal_arrest(deal)
            print("DONE!")
            
        

