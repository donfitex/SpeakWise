from accounts import views as accounts
from classroom import views as classroom
from core.views import health
from curriculum import views as curriculum
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from placement import views as placement

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

urlpatterns += [
    path("api/v1/courses/", curriculum.courses),
    path("api/v1/lessons/<uuid:pk>/", curriculum.lesson),
]

urlpatterns += [
    path("api/v1/placement-sessions/", placement.start),
    path("api/v1/placement-sessions/<uuid:pk>/answers/", placement.detail),
    path("api/v1/placement-sessions/<uuid:pk>/result/", placement.detail),
]

urlpatterns += [
    path("api/v1/lesson-sessions/", classroom.start),
    path("api/v1/lesson-sessions/<uuid:pk>/", classroom.detail),
    path("api/v1/lesson-sessions/<uuid:pk>/turns/", classroom.answer),
]
