# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView, View
from django.views.generic.base import ContextMixin, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.edit import FormView

from mis_template.services.feature import FeatureService


def default_context_data(context_data):
    enabled_feature_list = FeatureService().get_all()
    context_data['ENABLED_FEATURE_LIST'] = enabled_feature_list
    context_data['show_default_filter_buttons'] = True
    return context_data


class TemplateGenericView(TemplateView):

    def get_context_data(self, **kwargs):
        context_data = super(TemplateGenericView, self).get_context_data(**kwargs)
        return default_context_data(context_data)


class TemplateList(ListView):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS

    def get_context_data(self, **kwargs):
        context_data = super(TemplateList, self).get_context_data(**kwargs)
        return default_context_data(context_data)


class TemplateFilteredList(FormMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS

    def get_context_data(self, **kwargs):
        context_data = super(TemplateFilteredList, self).get_context_data(**kwargs)
        return default_context_data(context_data)


class TemplateDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context_data = super(TemplateDetailView, self).get_context_data(**kwargs)
        return default_context_data(context_data)


class TemplateCreate(CreateView):
    def get_context_data(self, **kwargs):
        context_data = super(TemplateCreate, self).get_context_data(**kwargs)
        return default_context_data(context_data)


class TemplateUpdate(UpdateView):
    def get_context_data(self, **kwargs):
        context_data = super(TemplateUpdate, self).get_context_data(**kwargs)
        return default_context_data(context_data)


class TemplateDelete(DeleteView):
    def get_context_data(self, **kwargs):
        context_data = super(TemplateDelete, self).get_context_data(**kwargs)
        return default_context_data(context_data)


# ======== AUTHENTICATED VIEWS ======== #

class MyAuthenticatedTemplateView(PermissionRequiredMixin, ContextMixin, SuccessMessageMixin, View):
    def get_context_data(self, **kwargs):
        context_data = super(MyAuthenticatedTemplateView, self).get_context_data(**kwargs)
        context_data['username'] = self.request.user.username
        return default_context_data(context_data)


class MyAuthenticatedTemplate(PermissionRequiredMixin, ContextMixin, SuccessMessageMixin):
    def get_context_data(self, **kwargs):
        context_data = super(MyAuthenticatedTemplate, self).get_context_data(**kwargs)
        context_data['username'] = self.request.user.username
        return default_context_data(context_data)


class AuthenticatedTemplateList(MyAuthenticatedTemplateView, ListView):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS


class AuthenticatedTemplateFilteredList(MyAuthenticatedTemplateView, FormMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS


class AuthenticatedTemplateDetailView(MyAuthenticatedTemplateView, DetailView):
    pass


class AuthenticatedTemplateCreate(MyAuthenticatedTemplateView, CreateView):
    pass


class AuthenticatedTemplateUpdate(MyAuthenticatedTemplateView, UpdateView):
    pass


class AuthenticatedTemplateDelete(MyAuthenticatedTemplateView, DeleteView):
    pass


class AuthenticatedRedirectView(MyAuthenticatedTemplateView, RedirectView):
    pass


class AuthenticatedTemplateView(MyAuthenticatedTemplateView, TemplateView):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS


class AuthenticatedView(MyAuthenticatedTemplateView, View):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS


class AuthenticatedTemplateForm(MyAuthenticatedTemplateView, FormView):
    paginate_by = settings.DEFAULT_PAGINATION_OBJECTS
