from django.contrib import admin
from django.shortcuts import redirect
from django.contrib import messages
import secrets

from bx24.lib.services.client import Bx24Client
from bx24.models import BitrixAuth

@admin.register(BitrixAuth)
class BitrixAuthAdmin(admin.ModelAdmin):

    change_form_template = "admin/bx24/bitrixauth/change_form.html"

    readonly_fields = (
        'access_token',
        'refresh_token',
        'access_token_expires',
        'refresh_token_expires',
        'updated_at'
    )

    fieldsets = (
        ("Настройки подключения", {
            "fields": ("domain", "client_id", "client_secret", "redirect_uri")
        }),
        ("Запасной токен", {
            "fields": ("long_token",)
        }),
        ("Токены (заполняются автоматически)", {
            "fields": ("access_token", "refresh_token", "access_token_expires", "refresh_token_expires", "updated_at")
        }),
    )

    def response_change(self, request, obj):
        if "_get_tokens" in request.POST:
            return self._start_oauth(request, obj)
        if "_refresh_tokens" in request.POST:
            return self._refresh_tokens(request, obj)
        return super().response_change(request, obj)

    def _start_oauth(self, request, obj):
        if not obj.client_id or not obj.redirect_uri or not obj.domain:
            self.message_user(
                request,
                "Заполните client_id, redirect_uri и domain",
                level=messages.ERROR
            )
            return redirect(request.path)

        state = secrets.token_urlsafe(16)
        request.session['bitrix_oauth_state'] = state

        params = (
            f"?client_id={obj.client_id}"
            f"&response_type=code"
            f"&redirect_uri={obj.redirect_uri}"
            f"&state={state}"
        )
        return redirect(f"{obj.domain}/oauth/authorize/{params}")
    
    def _refresh_tokens(self, request, obj):
        if not obj.refresh_token:
            self.message_user(
                request,
                "Нет refresh_token. Сначала получите токены.",
                level=messages.ERROR
            )
            return redirect(request.path)

        if obj.is_refresh_token_expired():
            self.message_user(
                request,
                "Refresh token истёк. Нужно получить токены заново.",
                level=messages.ERROR
            )
            return redirect(request.path)

        try:
            client = Bx24Client()
            client._refresh_access_token()
            self.message_user(request, "Токены успешно обновлены!", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Ошибка: {e}", level=messages.ERROR)

        return redirect(request.path)
