from django.db import models
from django.utils import timezone

class BitrixAuth(models.Model):
    class Meta:
        verbose_name = "Аутентификационные данные Bitrix24"
        verbose_name_plural = "Аутентификационные данные Bitrix24"
    
    long_token = models.CharField(null=True,max_length=255)
    domain = models.CharField(null=True,max_length=255)
    client_id = models.CharField(null=True,max_length=255)
    client_secret = models.CharField(null=True,max_length=255)
    redirect_uri = models.CharField(null=True,max_length=255)
    refresh_token = models.CharField(null=True,max_length=2000)
    access_token = models.CharField(null=True,max_length=2000)
    refresh_token_expires = models.DateTimeField(null=True)
    access_token_expires = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_access_token_expired(self):
        if not self.access_token_expires:
            return True
        return timezone.now() >= self.access_token_expires

    def is_refresh_token_expired(self):
        if not self.refresh_token_expires:
            return True
        return timezone.now() >= self.refresh_token_expires
    
    def __str__(self):
        return "Интеграция Bitrix24"