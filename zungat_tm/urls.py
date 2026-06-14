from django.contrib import admin
from django.urls import path,include
from zungat_tm.views import healthcheck

urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path('admin/', admin.site.urls),
    path("apps/writeoff/",include("apps.domain.writeoff.urls")),
    path("apps/writeoff/",include("apps.domain.cencel_payment.urls")),
    path("apps/bitrix/",include("apps.integrations.bx24.urls")),
    # path("apps/",include("apps.domain.recovery.urls")),
    # path("apps/",include("apps.domain.installments.urls"))
    ]
