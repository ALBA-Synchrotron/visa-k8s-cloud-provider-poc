# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse_lazy

from object_template.forms.my_object_name import MyObjectNameForm
from object_template.forms.my_object_name_filter import MyObjectNameFilterForm
from object_template.labels.model import my_object_name as labels
from object_template.models import MyObjectName
from object_template.services.my_object_name import MyObjectNameService
from mis_template.utils.views import ListAuthenticated, DetailAuthenticated, CreateAuthenticated, UpdateAuthenticated, \
    DeleteAuthenticated

default_model_class = MyObjectName
default_filter_form_class = MyObjectNameFilterForm
default_form_class = MyObjectNameForm
default_service = MyObjectNameService()
template_directory_name = labels.APP_NAME + '/' + labels.MODEL_NAME + '/'
default_permission_app_label_name = 'object_template'
default_permission_content_type_name = 'my_object_name'


class List(ListAuthenticated):
    model = default_model_class
    form_class = default_filter_form_class
    filter_form_class = default_filter_form_class
    template_name = template_directory_name + 'list.html'
    paginate_by = 10
    service = default_service
    filter_excluded_fields = []
    list_excluded_fields = []
    labels = labels
    permission_required = '%s.view_%s' % (default_permission_app_label_name, default_permission_content_type_name)

    def get_context_data(self, *args, **kwargs):
        context_data = super(List, self).get_context_data(**kwargs)
        context_data['can_add_object'] = True
        context_data['show_button_column'] = True
        context_data['object_detail_available'] = True
        context_data['object_edit_available'] = True
        return context_data

    def get_queryset(self):
        search_filter = dict(self.request.GET)
        search_filter.pop('page', None)
        return self.service.get_filtered(search_filter, like_fields=['name'])


class Detail(DetailAuthenticated):
    model = default_model_class
    template_name = template_directory_name + 'detail.html'
    excluded_fields = []
    extra_fields = 0
    labels = labels
    permission_required = '%s.view_%s' % (default_permission_app_label_name, default_permission_content_type_name)


class Create(CreateAuthenticated):
    model = default_model_class
    form_class = default_form_class
    template_name = template_directory_name + 'form.html'
    excluded_fields = []
    extra_fields = 0
    labels = labels
    success_url = reverse_lazy(labels.MODEL_NAME + '_list')
    permission_required = '%s.add_%s' % (default_permission_app_label_name, default_permission_content_type_name)


class Update(UpdateAuthenticated):
    model = default_model_class
    form_class = default_form_class
    template_name = template_directory_name + 'form.html'
    excluded_fields = []
    extra_fields = 0
    labels = labels
    success_url = reverse_lazy(labels.MODEL_NAME + '_list')
    permission_required = '%s.change_%s' % (default_permission_app_label_name, default_permission_content_type_name)


class Delete(DeleteAuthenticated):
    model = default_model_class
    template_name = template_directory_name + 'delete.html'
    labels = labels
    success_url = reverse_lazy(labels.MODEL_NAME + '_list')
    permission_required = '%s.delete_%s' % (default_permission_app_label_name, default_permission_content_type_name)
