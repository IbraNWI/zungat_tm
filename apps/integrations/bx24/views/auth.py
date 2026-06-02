import requests
import secrets
from datetime import timedelta

from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone


from apps.integrations.bx24.lib.models.auth import BitrixAuth


def bitrix_connect(request):
    """
    Шаг 1 — редиректим пользователя на страницу авторизации Битрикса.
    Пользователь нажимает "Подключить" → попадает сюда → улетает на Битрикс.
    """
    auth = BitrixAuth.objects.first()

    if not auth or not auth.client_id or not auth.redirect_uri:
        return HttpResponse("Сначала заполните client_id и redirect_uri в админке", status=400)

    # Сохраняем state в сессию для защиты от CSRF
    state = secrets.token_urlsafe(16)
    request.session['bitrix_oauth_state'] = state

    params = (
        f"?client_id={auth.client_id}"
        f"&response_type=code"
        f"&redirect_uri={auth.redirect_uri}"
        f"&state={state}"
    )
    bitrix_domain = auth.domain
    return redirect(f"{bitrix_domain}/oauth/authorize/{params}")

def bitrix_callback(request):
    """
    Шаг 2 — Битрикс редиректит сюда с ?code=XXXX.
    Меняем code на токены и сохраняем в базу.
    """
    # Проверяем state
    state = request.GET.get('state')
    if state != request.session.get('bitrix_oauth_state'):
        return HttpResponse("Ошибка безопасности: state не совпадает", status=403)

    code = request.GET.get('code')
    if not code:
        return HttpResponse("Ошибка: code не получен от Битрикса", status=400)

    auth = BitrixAuth.objects.first()
    if not auth:
        return HttpResponse("Ошибка: настройки интеграции не найдены", status=400)

    # Меняем code на токены
    response = requests.post('https://oauth.bitrix.info/oauth/token/', data={
        'grant_type': 'authorization_code',
        'client_id': auth.client_id,
        'client_secret': auth.client_secret,
        'redirect_uri': auth.redirect_uri,
        'code': code,
    })

    if response.status_code != 200:
        return HttpResponse(f"Ошибка от Битрикса: {response.text}", status=400)

    data = response.json()

    # Сохраняем токены в базу
    now = timezone.now()
    auth.access_token = data['access_token']
    auth.refresh_token = data['refresh_token']
    auth.token_expires = now + timedelta(seconds=data['expires_in'])
    auth.refresh_token_expires = now + timedelta(days=180)
    auth.save()

    # Чистим state из сессии
    del request.session['bitrix_oauth_state']

    return redirect('/admin')  # редиректим куда нужно