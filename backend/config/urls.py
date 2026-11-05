from accounts import views as accounts
from core.views import health
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", health),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]


urlpatterns += [
    path("api/v1/auth/csrf/", accounts.csrf),
    path("api/v1/auth/register/", accounts.register),
    path("api/v1/auth/login/", accounts.sign_in),
    path("api/v1/auth/logout/", accounts.sign_out),
    path("api/v1/auth/password-reset/", accounts.password_reset),
    path("api/v1/auth/password-reset/confirm/", accounts.reset_confirm),
    path("api/v1/learners/me/", accounts.me),
    path("api/v1/learners/me/consent/", accounts.consent),
]
