from urllib import parse
from allauth.account.views import LogoutFunctionalityMixin
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import re
import jwt
from mis_template.sso_authentication.session_store import SessionStore
from django.conf import settings


class LocalSessionSignOutView(LogoutFunctionalityMixin, APIView):

    def post(self, *args, **kwargs):
        body_unicode = self.request.body.decode('utf-8')
        if body_unicode:
            jwt_logout_token = re.search("(logout_token=)(.*)", body_unicode)
            if jwt_logout_token:
                logout_token = jwt.decode(jwt_logout_token.group(2), algorithms=settings.JWT_DEFAULT_ALGORITHMS_LIST,
                                          options=settings.JWT_DEFAULT_OPTS)
                if logout_token:
                    SessionStore.close_session_by_subject_uid(logout_token['sub'])
                    return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


def login_redirect_to_keycloak(request):
    login = reverse('openid_connect_login', kwargs={'provider_id': 'alba-sso'})
    next_page = request.GET.get("next", "/")
    url_params = {
        "process": "login",
        "next": next_page
    }
    suffix = parse.urlencode(url_params)
    return redirect(f"{login}?{suffix}")


def logout_redirect_to_keycloak(_):
    return redirect(settings.SSO_LOGOUT_REDIRECT_URL.format(settings.APP_HOST))
