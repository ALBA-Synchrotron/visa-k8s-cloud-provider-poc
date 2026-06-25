"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include, re_path
from allauth.socialaccount.providers.openid_connect import views as allauth_oidc_views
from mis_template.sso_authentication.views import login_redirect_to_keycloak, LocalSessionSignOutView, \
    logout_redirect_to_keycloak
sso_urlpatterns = [
    path("accounts/login/", login_redirect_to_keycloak, name="account_login_alba_sso"),
    path("admin/login/", login_redirect_to_keycloak, name="admin_login_alba_sso"),
    path("admin/logout/", logout_redirect_to_keycloak, name="account_logout"),
    path("sso/logout/", LocalSessionSignOutView.as_view(), name="account_logout"),
    path("accounts/logout/", logout_redirect_to_keycloak, name="sso_logout"),
    re_path(r"^(?P<provider_id>[^/]+)/", include(
        [
            path("login/", allauth_oidc_views.login, name="openid_connect_login", ),
            path("login/callback/", allauth_oidc_views.callback, name="openid_connect_callback", ),
        ]
    )),
]



app_urlpatterns = [
    path('', include('cloud_provider.urls.generic')),
]

admin_urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns: list = []

if not os.getenv("OIDC_AUTH_DISABLE") == "1":
    urlpatterns = sso_urlpatterns

urlpatterns = urlpatterns + app_urlpatterns + admin_urlpatterns
