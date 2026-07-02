from django.db import models


class DriverSyncState(models.Model):
    driver_id = models.IntegerField(unique=True)
    last_processed_operation_id = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "driver_sync_state"