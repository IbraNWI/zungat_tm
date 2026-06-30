from django.db import IntegrityError
import random
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

class DepositArrestError(Exception):
    pass


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
            print(f'[DEBUG INFO] deal {deal.id} arrest sum is {deal.total_arest_sum}\n')
        deals_with_arrest = [deal for deal in deals if deal.total_arest_sum != None]
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
        
        finish_time = datetime.now(timezone.utc)
        last_payment_date = datetime.fromisoformat(last_payment_date)

        operations = self.tm_client.operation.get(
            driver_id=driver_id,
            start_time=last_payment_date,
            finish_time=finish_time
        )

        receipt_operations = [ oper for oper in operations if oper.oper_type == "receipt"]

        for oper in receipt_operations: 
            oper.driver_id = driver_id #driver_id не хранится в Operation, но я получаю его из payment_rule  
        
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
            driver_id=deposit_operation.driver_id,
            operation_id=deposit_operation.id,
            available_funds=deposit_operation.sum,
            deposit_date=deposit_operation.create_time
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
                for d in arrested_deposits:
                    print(f'found in arrested_deposits {d}')
                return available_deposits
        
        arrested_deposits_ids = [ad.operation_id for ad in arrested_deposits]

        for deposit_operation in deposits_operations:
            if deposit_operation.id in arrested_deposits_ids:
                continue
            else:
                new_arrested_deposit = self.create_new_arrested_deposit(deposit_operation)
                print(f'created new arrested deposit by {deposit_operation} and here it is {new_arrested_deposit}')
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
            company_id=deal.company_id,
            contact_id=deal.contact_id,
            contact_ids=deal.contact_ids,
            category_id=deal.category_id,
            stage_id=success_stage_id,
            assigned_by_id=deal.assigned_by_id,
            opportunity=payment_amount,
            arest_sum=0,
            deal_id=deal.id
        )
        return payment

    def process_deposits_to_pay_deal_arrest(self,deal_with_arrest : Deal):
        """
        Ищу дату последнего fact payment по deal в payment rule, 
        Но я не уверен что дата последнего fact payment всегда хранится там, 
        что если платеж был совершен без payment rule? такое вообще возможно?
        """

        last_payment_date = self.get_deal_last_payment_date(deal_with_arrest)
        print(f'[DEBUG INFO] Дата последнего платежа по рассрочке {last_payment_date}')

        driver_id = self.get_deal_driver_id(deal_with_arrest)
        deal_arrest_amount = deal_with_arrest.total_arest_sum
        if last_payment_date == None:
            print(f'[ERROR] - отсутствует дата последнего платежа в payment_rule')
            return None
            #raise DepositArrestError
        if driver_id == None:
            print(f'[ERROR] - отсутствует driver_id')
            return None
            #raise DepositArrestError

        print(f'[DEBUG INFO] - looking for driver {driver_id} deposits after {last_payment_date}')
        new_deposits = self.get_driver_deposits_after(driver_id,last_payment_date)
        print(f'[DEBUG INFO] - Found {len(new_deposits)} deposits')

        print(f'[DEBUG INFO] - looking for driver {driver_id} arrested deposits after {last_payment_date}')
        arrested_deposits = self.get_arrested_deposits_after(driver_id,last_payment_date)
        print(f'[DEBUG INFO] - Found {len(arrested_deposits)} arrested deposits')

        print(f'[DEBUG INFO] - looking for available to pay arrest deposits')
        available_deposits_to_payment = self.get_available_deposits_to_payment(new_deposits, arrested_deposits, deal_arrest_amount)
        print(f'[DEBUG INFO] - Found {len(available_deposits_to_payment)} deposits with available funds')

        arested_deposits_available_funds = 0
        used_deposits = []

        for deposit in available_deposits_to_payment:
            arested_deposits_available_funds += deposit.available_funds
            if arested_deposits_available_funds >= deal_arrest_amount:

                remaining_funds = arested_deposits_available_funds - deal_arrest_amount

                if remaining_funds < deposit.available_funds:
                    used_deposits.append({"deposit" : deposit, "spent_amount" : deposit.available_funds - remaining_funds})
                    deposit.available_funds = remaining_funds   ## SETTER FOR PROTECTION
                break
            else:
                used_deposits.append({"deposit" : deposit, "spent_amount" : deposit.available_funds})
                deposit.available_funds = 0 ## SETTER FOR PROTECTION TODO

        if arested_deposits_available_funds <= 0:
            print('no available funds to pay arrest')
            return None
        else:
            print(f'[DEBUG INFO] arested deposits available funds is {arested_deposits_available_funds}')

        if arested_deposits_available_funds > deal_arrest_amount:
            payment_amount = deal_arrest_amount
        else:
            payment_amount = arested_deposits_available_funds 
        payment_title = f"Закрытие ареста сделки {deal_with_arrest.id} на сумму {payment_amount}"
        print(f'[DEBUG INFO] - creating new fact payment titled {payment_title}\n')
        new_payment = self.create_fact_payment(deal_with_arrest,payment_amount,payment_title)
        if new_payment != None:
            if INDEV:
                print(f"[INFO] - used deposits is {used_deposits} \n")
                print(f"[WARNING] - changes was never commited")
                print(f"[SUCCESS] - new payment is {new_payment} \n")
                input('Press Enter to continue to next deal')
            else:
                #new_fact_payment = self.bx_client.fact_payment.add(new_payment) #uncomment when tested

                for deposit in used_deposits: # saving changes
                    #deposit["deposit"].fact_payments[str(new_fact_payment.id)] = deposit["spent_amount"] #uncomment when tested
                    deposit["deposit"].fact_payments[f"testRandomId{random.randint(10000000,99999999)}"] = deposit["spent_amount"]
                    try:
                        deposit["deposit"].save()
                    except IntegrityError:
                        print('!!!! THAT SHOULD NEVER HAPPED, check for bugs  !!!!!')
                        print(f'all arrested deposits : {list(ArrestedDeposit.objects.all())}')
                        print(f'new arrested deposit is {deposit.driver_id}, {deposit.operation_id }')
                        print('aborting an attemt to create new arested deposid with already existing id or no driver_id')

    def execute(self):

        print(f'[Info] gathering all deals ----\n')
        all_deals = self.get_deals()
        print(f'[Info] filtering deals with arrests\n')
        deals_with_arrest = self.filter_deals_with_arrest(all_deals)

        for deal in deals_with_arrest:
            print(f'[INFO] proccessing deal\n\n {deal} \n')
            self.process_deposits_to_pay_deal_arrest(deal)
            
        

