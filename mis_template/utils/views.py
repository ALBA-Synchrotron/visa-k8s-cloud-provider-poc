# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mis_template.services.label import LabelService
from mis_template.utils.filter import request_filter_dict_to_initial_value_dict
from mis_template.utils.template_views import AuthenticatedTemplateFilteredList, TemplateDetailView, \
    AuthenticatedTemplateDetailView, TemplateCreate, AuthenticatedTemplateCreate, AuthenticatedTemplateUpdate, \
    TemplateUpdate, AuthenticatedTemplateDelete, TemplateDelete, TemplateFilteredList
from cloud_provider.labels.generic import generic as labels


def default_context_data(context_data, my_labels):
    context_data['labels'] = my_labels
    return context_data


# Generic LIST functions
def get_list_headers(context_data, filter_excluded_fields_list, list_excluded_fields_list, filter_boolean_fields,
                     model):
    context_data['list_headers'] = []
    context_data['filter_excluded_fields'] = filter_excluded_fields_list
    context_data['list_excluded_fields'] = list_excluded_fields_list
    context_data['filter_boolean_fields'] = filter_boolean_fields
    for header in labels.LIST_HEADERS:
        if header not in context_data['list_headers']:
            context_data['list_headers'].append(header)
    for field in model._meta.get_fields():
        if field.name and field.name not in context_data['list_excluded_fields'] and field.name not in context_data[
            'list_headers'] and hasattr(field, 'verbose_name'):
            context_data['list_headers'].append(field.verbose_name)
    context_data['list_excluded_fields'] = list(
        map(lambda excluded_fields: excluded_fields.replace('_', ' ').lower(), context_data['list_excluded_fields']))

    return context_data


def default_list_get_queryset(get_data, service):
    search_filter = dict(get_data)
    search_filter.pop('page', None)
    return service.get_filtered(search_filter)


def get_label_list(context_data):
    context_data['label_list'] = LabelService().get_all()
    return context_data


def default_list_get_context_data(context_data, my_labels, my_filter_excluded_fields, my_list_excluded_fields,
                                  my_filter_boolean_fields, my_model, my_request, my_filter_form_class,
                                  my_fk_fields_list, my_fk_fields_dict, my_link_fields, my_html_fields,
                                  my_m2m_fields_list, my_m2m_fields_dict, my_overwrite_field_value):
    context_data = default_context_data(context_data, my_labels)
    context_data = get_list_headers(context_data, my_filter_excluded_fields, my_list_excluded_fields,
                                    my_filter_boolean_fields, my_model)
    context_data = get_label_list(context_data)

    context_data['fk_fields_list'] = my_fk_fields_list
    context_data['fk_fields_dict'] = my_fk_fields_dict
    context_data['m2m_fields_list'] = my_m2m_fields_list
    context_data['m2m_fields_dict'] = my_m2m_fields_dict
    context_data['link_fields'] = my_link_fields
    context_data['html_fields'] = my_html_fields
    context_data['overwrite_field_value'] = my_overwrite_field_value

    initial_values = request_filter_dict_to_initial_value_dict(dict(my_request.GET))
    if my_filter_form_class:
        if initial_values:
            context_data['form'] = my_filter_form_class(initial=initial_values)
        else:
            context_data['form'] = my_filter_form_class()

    return context_data


# Generic Detail functions
def default_detail_get_context_data(context_data, my_labels, my_extra_fields, my_excluded_fields, my_fk_fields_list,
                                    my_fk_fields_dict, my_link_fields, my_m2m_fields_list, my_m2m_fields_dict,
                                    my_html_fields, my_overwrite_field_value, my_full_width_fields_list):
    context_data = default_context_data(context_data, my_labels)
    context_data['extra_fields'] = my_extra_fields
    context_data['excluded_fields'] = my_excluded_fields
    if context_data['excluded_fields']:
        context_data['excluded_fields'] = list(
            map(lambda excluded_fields: excluded_fields.replace('_', ' ').lower(), context_data['excluded_fields']))
    context_data['fk_fields_list'] = my_fk_fields_list
    context_data['fk_fields_dict'] = my_fk_fields_dict
    context_data['link_fields'] = my_link_fields
    context_data['m2m_fields_list'] = my_m2m_fields_list
    context_data['m2m_fields_dict'] = my_m2m_fields_dict
    context_data['html_fields'] = my_html_fields
    context_data['overwrite_field_value'] = my_overwrite_field_value
    context_data['full_width_fields_list'] = my_full_width_fields_list
    return context_data


# Generic Create functions
def default_create_get_context_data(context_data, my_labels, my_extra_fields, my_excluded_fields, formset_names,
                                    formset_classes, my_m2m_fields_list, my_full_width_fields, post_data):
    context_data = default_context_data(context_data, my_labels)
    context_data['extra_fields'] = my_extra_fields
    context_data['excluded_fields'] = my_excluded_fields
    context_data['m2m_fields_list'] = my_m2m_fields_list
    context_data['full_width_fields'] = my_full_width_fields

    if post_data:
        for index, formset_name in enumerate(formset_names):
            context_data[formset_name] = formset_classes[index](post_data)
    else:
        for index, formset_name in enumerate(formset_names):
            context_data[formset_name] = formset_classes[index]()

    return context_data


# Generic Update functions
def default_update_get_context_data(context_data, my_labels, my_extra_fields, my_excluded_fields, my_read_only_fields,
                                    formset_names, formset_classes, my_m2m_fields_list, my_full_width_fields, my_object,
                                    post_data):
    context_data = default_context_data(context_data, my_labels)
    context_data['extra_fields'] = my_extra_fields
    context_data['excluded_fields'] = my_excluded_fields
    context_data['read_only_fields'] = my_read_only_fields
    context_data['m2m_fields_list'] = my_m2m_fields_list
    context_data['full_width_fields'] = my_full_width_fields

    if post_data:
        for index, formset_name in enumerate(formset_names):
            context_data[formset_name] = formset_classes[index](post_data, instance=my_object)
    else:
        for index, formset_name in enumerate(formset_names):
            context_data[formset_name] = formset_classes[index](instance=my_object)

    return context_data


# Generic Delete functions
def default_delete_get_context_data(context_data, my_labels):
    context_data = default_context_data(context_data, my_labels)
    return context_data


class ListAuthenticated(AuthenticatedTemplateFilteredList):
    logger = logging.getLogger(__name__)

    model = None
    form_class = None
    filter_form_class = None
    template_name = 'list.html'
    paginate_by = 10
    service = None
    filter_excluded_fields = []
    list_excluded_fields = []
    filter_boolean_fields = []
    html_fields = []
    fk_fields_list = []
    fk_fields_dict = None
    m2m_fields_list = []
    m2m_fields_dict = None
    link_fields = []
    overwrite_field_value = {}
    labels = labels

    def get_queryset(self):
        return default_list_get_queryset(self.request.GET, self.service)

    def get_context_data(self, *args, **kwargs):
        context_data = super(ListAuthenticated, self).get_context_data(**kwargs)
        context_data = default_list_get_context_data(context_data, self.labels, self.filter_excluded_fields,
                                                     self.list_excluded_fields, self.filter_boolean_fields, self.model,
                                                     self.request, self.filter_form_class, self.fk_fields_list,
                                                     self.fk_fields_dict, self.link_fields, self.html_fields,
                                                     self.m2m_fields_list, self.m2m_fields_dict,
                                                     self.overwrite_field_value)
        return context_data


class ListNotAuthenticated(TemplateFilteredList):
    logger = logging.getLogger(__name__)

    model = None
    form_class = None
    filter_form_class = None
    template_name = 'list.html'
    paginate_by = 10
    service = None
    filter_excluded_fields = []
    list_excluded_fields = []
    filter_boolean_fields = []
    fk_fields_list = []
    fk_fields_dict = None
    link_fields = []
    overwrite_field_value = {}
    labels = labels

    def get_queryset(self):
        return default_list_get_queryset(self.request.GET, self.service)

    def get_context_data(self, *args, **kwargs):
        context_data = super(ListNotAuthenticated, self).get_context_data(**kwargs)
        context_data = default_list_get_context_data(context_data, self.labels, self.filter_excluded_fields,
                                                     self.list_excluded_fields, self.filter_boolean_fields, self.model,
                                                     self.request, self.filter_form_class, self.fk_fields_list,
                                                     self.fk_fields_dict, self.link_fields, self.overwrite_field_value)

        return context_data


class DetailAuthenticated(AuthenticatedTemplateDetailView):
    logger = logging.getLogger(__name__)

    model = None
    template_name = 'detail.html'
    excluded_fields = []
    full_width_fields_list = []
    extra_fields = 0
    fk_fields_list = []
    fk_fields_dict = None
    link_fields = []
    m2m_fields_list = []
    m2m_fields_dict = None
    html_fields = []
    overwrite_field_value = {}
    labels = labels

    def get_context_data(self, *args, **kwargs):
        context_data = super(DetailAuthenticated, self).get_context_data(**kwargs)
        context_data = default_detail_get_context_data(context_data, self.labels, self.extra_fields,
                                                       self.excluded_fields, self.fk_fields_list, self.fk_fields_dict,
                                                       self.link_fields, self.m2m_fields_list, self.m2m_fields_dict,
                                                       self.html_fields, self.overwrite_field_value,
                                                       self.full_width_fields_list)
        return context_data


class DetailNotAuthenticated(TemplateDetailView):
    logger = logging.getLogger(__name__)

    model = None
    template_name = 'detail.html'
    excluded_fields = []
    full_width_fields_list = []
    extra_fields = 0
    fk_fields_list = []
    fk_fields_dict = None
    link_fields = []
    m2m_fields_list = []
    m2m_fields_dict = None
    html_fields = []
    overwrite_field_value = {}
    labels = labels

    def get_context_data(self, *args, **kwargs):
        context_data = super(DetailNotAuthenticated, self).get_context_data(**kwargs)
        context_data = default_detail_get_context_data(context_data, self.labels, self.extra_fields,
                                                       self.excluded_fields, self.fk_fields_list, self.fk_fields_dict,
                                                       self.link_fields, self.m2m_fields_list, self.m2m_fields_dict,
                                                       self.html_fields, self.overwrite_field_value,
                                                       self.full_width_fields_list)
        return context_data


class CreateAuthenticated(AuthenticatedTemplateCreate):
    logger = logging.getLogger(__name__)

    model = None
    form_class = None
    template_name = 'form.html'
    excluded_fields = []
    extra_fields = 0
    labels = labels
    success_url = ''
    formset_names = []
    formset_classes = []
    m2m_fields_list = []
    full_width_fields = []

    def get_context_data(self, *args, **kwargs):
        context_data = super(CreateAuthenticated, self).get_context_data(**kwargs)
        context_data = default_create_get_context_data(context_data, self.labels, self.extra_fields,
                                                       self.excluded_fields, self.formset_names, self.formset_classes,
                                                       self.m2m_fields_list, self.full_width_fields, self.request.POST)
        return context_data

    def get_success_url(self):
        return self.success_url

    @staticmethod
    def handle_attachment_form_errors(object_attachment_list):
        for object_attachment in object_attachment_list.forms:
            if object_attachment.errors and 'file' in object_attachment.errors and object_attachment.errors['file']:
                object_attachment.fields['file'].widget.attrs.update({'error': object_attachment.errors['file'][0]})


class CreateNotAuthenticated(TemplateCreate):
    logger = logging.getLogger(__name__)

    model = None
    form_class = None
    template_name = 'form.html'
    excluded_fields = []
    extra_fields = 0
    labels = labels
    success_url = ''
    formset_names = []
    formset_classes = []
    m2m_fields_list = []
    full_width_fields = []

    def get_context_data(self, *args, **kwargs):
        context_data = super(CreateNotAuthenticated, self).get_context_data(**kwargs)
        context_data = default_create_get_context_data(context_data, self.labels, self.extra_fields,
                                                       self.excluded_fields, self.formset_names, self.formset_classes,
                                                       self.m2m_fields_list, self.full_width_fields, self.request.POST)
        return context_data

    def get_success_url(self):
        return self.success_url


class UpdateAuthenticated(AuthenticatedTemplateUpdate):
    logger = logging.getLogger(__name__)

    model = None
    form_class = None
    template_name = 'form.html'
    excluded_fields = []
    read_only_fields = []
    extra_fields = 0
    labels = labels
    success_url = ''
    formset_names = []
    formset_classes = []
    m2m_fields_list = []
    full_width_fields = []

    def get_context_data(self, *args, **kwargs):
        context_data = super(UpdateAuthenticated, self).get_context_data(**kwargs)
        context_data = default_update_get_context_data(context_data, self.labels, self.extra_fields,
                                                       self.excluded_fields, self.read_only_fields, self.formset_names,
                                                       self.formset_classes, self.m2m_fields_list,
                                                       self.full_width_fields, self.object, self.request.POST)
        return context_data

    def get_success_url(self):
        return self.success_url

    @staticmethod
    def handle_attachment_form_errors(object_attachment_list):
        for object_attachment in object_attachment_list.forms:
            if object_attachment.errors and 'file' in object_attachment.errors and object_attachment.errors['file']:
                object_attachment.fields['file'].widget.attrs.update({'error': object_attachment.errors['file'][0]})


class UpdateNotAuthenticated(TemplateUpdate):
    logger = logging.getLogger(__name__)

    model = None
    form_class = None
    template_name = 'form.html'
    excluded_fields = []
    read_only_fields = []
    extra_fields = 0
    labels = labels
    success_url = ''
    formset_names = []
    formset_classes = []
    m2m_fields_list = []
    full_width_fields = []

    def get_context_data(self, *args, **kwargs):
        context_data = super(UpdateNotAuthenticated, self).get_context_data(**kwargs)
        context_data = default_update_get_context_data(context_data, self.labels, self.extra_fields,
                                                       self.excluded_fields, self.read_only_fields, self.formset_names,
                                                       self.formset_classes, self.m2m_fields_list,
                                                       self.full_width_fields, self.object, self.request.POST)
        return context_data

    def get_success_url(self):
        return self.success_url


class DeleteAuthenticated(AuthenticatedTemplateDelete):
    logger = logging.getLogger(__name__)

    model = None
    labels = labels
    success_url = ''
    template_name = 'delete.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(DeleteAuthenticated, self).get_context_data(**kwargs)
        context_data = default_delete_get_context_data(context_data, self.labels)
        return context_data

    def get_success_url(self):
        return self.success_url


class DeleteNotAuthenticated(TemplateDelete):
    logger = logging.getLogger(__name__)

    model = None
    labels = labels
    success_url = ''
    template_name = 'delete.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(DeleteNotAuthenticated, self).get_context_data(**kwargs)
        context_data = default_delete_get_context_data(context_data, self.labels)
        return context_data

    def get_success_url(self):
        return self.success_url
