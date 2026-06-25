# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, \
    DestroyAPIView


class CSRFExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CSRFExemptSSOAuthenticatedView(GenericAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedView, self).dispatch(*args, **kwargs)


class CSRFExemptView(GenericAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptView, self).dispatch(*args, **kwargs)


class CSRFExemptBasicAuthenticatedView(GenericAPIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptBasicAuthenticatedView, self).dispatch(*args, **kwargs)


class CSRFExemptListAPIView(ListAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptListAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptSSOAuthenticatedListAPIView(ListAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedListAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptBasicAuthenticatedListAPIView(ListAPIView):
    authentication_classes = (BasicAuthentication, CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptBasicAuthenticatedListAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptRetrieveAPIView(RetrieveAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptRetrieveAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptBasicAuthenticatedRetrieveAPIView(RetrieveAPIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptBasicAuthenticatedRetrieveAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptSSOAuthenticatedRetrieveAPIView(PermissionRequiredMixin, RetrieveAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedRetrieveAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptCreateAPIView(CreateAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptCreateAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptSSOAuthenticatedCreateAPIView(CreateAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedCreateAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptSSOAuthenticatedAPIView(PermissionRequiredMixin, GenericAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptSSOAuthenticatedUpdateAPIView(PermissionRequiredMixin, UpdateAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedUpdateAPIView, self).dispatch(*args, **kwargs)


class CSRFExemptSSOAuthenticatedDestroyAPIView(DestroyAPIView):
    authentication_classes = (CSRFExemptSessionAuthentication,)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptSSOAuthenticatedDestroyAPIView, self).dispatch(*args, **kwargs)
