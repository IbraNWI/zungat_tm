from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("apps/writeoff/",include("apps.domain.writeoff.urls")),
    # path("apps/",include("apps.domain.recovery.urls")),
    # path("apps/",include("apps.domain.installments.urls"))
    ]
