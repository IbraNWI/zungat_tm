from django.db import models
from apps.integrations.tm_driver.lib.schemas.operation import Operation
from django.utils import timezone
# Create your models here.


class ArrestedDeposit(models.Model):

    id = models.IntegerField(primary_key=True)
    driver_id = models.IntegerField()
    operation_id = models.IntegerField(unique=True)
    _available_funds = models.FloatField()
    deposit_date = models.DateTimeField(default=timezone.now)
    fact_payments = models.JSONField(default=dict)


    @property
    def available_funds(self):
        return self._available_funds

    @available_funds.setter
    def available_funds(self,value):
        if self._available_funds != None:
            if value <= self._available_funds:
                self._available_funds = value
            else:
                print('Unable to raise available_funds of the arrested deposit')
        else:
            self._available_funds = value
    
    def is_fully_spent(self) -> bool:
        if self.available_funds > 0:
            return False
        else:
            return True

    def __str__(self):
        return f"ArrestedDeposit ( driver_id={self.driver_id},operation_id={self.operation_id}, available_funds={self.available_funds}, deposit_date={self.deposit_date},fact_payments={self.fact_payments}"

    
