from django.db import models

class TaxiMasterAuth(models.Model):
    class Meta:
        verbose_name = "Аутентификационные данные TaxiMaster API"
        verbose_name_plural = "Аутентификационные данные TaxiMaster API"

    host = models.CharField(max_length=255, help_text="https://ip:port")
    secret_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TaxiMaster — {self.host}"