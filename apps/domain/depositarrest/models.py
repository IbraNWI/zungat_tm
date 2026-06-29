from django.db import models
from apps.integrations.tm_driver.lib.schemas.operation import Operation

# Create your models here.


class ArrestedDeposit(models.Model):

    id = models.IntegerField(primary_key=True)
    operation_id = models.IntegerField(unique=True)
    available_funds = models.FloatField(default=0.0)
    
    def is_fully_spent(self) -> bool:
        if self.available_funds > 0:
            return False
        else:
            return True

    

    
