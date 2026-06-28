import requests
from threading import Lock
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from apps.integrations.bx24.lib.models.auth import BitrixAuth
from apps.integrations.bx24.lib.services.crm.crm_client import (
    ContactClient,
    CompanyClient,
    DealClient,
    LeadClient,
    PaymentRuleClient,
    FactFapymentClient,
    PlanPaymentClient
)
from apps.integrations.bx24.lib.services.event.event_client import EventClient


class Bx24Client:

    def __init__(self):
        self._lock = Lock()
        self._load_auth()
        self._init_session()
        self._init_subclients()

    def _load_auth(self):
        self.auth = BitrixAuth.objects.first()
        if not self.auth:
            raise Exception("Настройки интеграции Битрикс24 не найдены")
        self.bitrix_domain = self.auth.domain

    def _init_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _init_subclients(self):
        self.contact = ContactClient(self)
        self.company = CompanyClient(self)
        self.lead = LeadClient(self)
        self.deal = DealClient(self)
        self.event = EventClient(self)
        self.plan_payment = PlanPaymentClient(self)
        self.fact_payment = FactFapymentClient(self)
        self.payment_rule = PaymentRuleClient(self)

    def _is_access_token_expiring(self):
        """Токен истёк или истекает в ближайшие 5 минут."""
        if not self.auth.access_token_expires:
            return True
        return self.auth.access_token_expires - timezone.now() < timedelta(minutes=5)

    def _refresh_access_token(self):
        """Обновляем access_token через refresh_token."""

        if self.auth.is_refresh_token_expired():
            raise Exception(
                "Refresh token истёк. Необходимо переподключить интеграцию Битрикс24."
            )

        response = requests.post('https://oauth.bitrix.info/oauth/token/', data={
            'grant_type': 'refresh_token',
            'client_id': self.auth.client_id,
            'client_secret': self.auth.client_secret,
            'refresh_token': self.auth.refresh_token,
        })

        if response.status_code != 200:
            raise Exception(f"Ошибка обновления токена: {response.text}")

        data = response.json()
        now = timezone.now()

        self.auth.access_token = data['access_token']
        self.auth.refresh_token = data['refresh_token']
        self.auth.access_token_expires = now + timedelta(seconds=data['expires_in'])
        self.auth.refresh_token_expires = now + timedelta(days=180)
        self.auth.save()

    def _ensure_valid_token(self):
        """
        Проверяем токен перед каждым запросом.
        select_for_update защищает от race condition при нескольких воркерах.
        """
        with self._lock:
            with transaction.atomic():
                self.auth = BitrixAuth.objects.select_for_update().first()

                if self._is_access_token_expiring():
                    self._refresh_access_token()

    def _get_url(self, method: str) -> str:
        """
        Формируем URL для запроса.
        Если есть OAuth-токены — используем их.
        Если нет — падаем на long_token как запасной вариант.
        """
        if self.auth.access_token and self.bitrix_domain:
            return f"{self.bitrix_domain}/rest/{method}"

        if self.auth.long_token:
            return f"{self.auth.long_token}{method}"

        raise Exception("Нет доступного способа авторизации. Заполните токены или подключите OAuth.")

    def _request(self, method: str, params: dict):

        # Если есть OAuth — проверяем и при необходимости обновляем токен
        if self.auth.access_token and self.auth.refresh_token:
            self._ensure_valid_token()
            params['auth'] = self.auth.access_token

        url = self._get_url(method)
        response = self.session.post(
            url=url,
            json=params
        )
        return self._check_response(response)

    def _check_response(self, response):

        if response.status_code // 100 == 4:
            print("Ошибка клиента")
            print(response.json())

        elif response.status_code // 100 == 5:
            print("Ошибка сервера")

        elif response.status_code // 100 == 2:
            return response.json()