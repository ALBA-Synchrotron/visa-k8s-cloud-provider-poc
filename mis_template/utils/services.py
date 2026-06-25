# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from datetime import datetime

from django.db.models.functions import Cast

from cloud_provider.labels.generic import generic as labels

from django.db.models import F, IntegerField, QuerySet
from django.utils import timezone


class GenericService:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.model_name: str = ''
        self.model_class = None
        self.id_not_null: str = 'Id should not be null'
        self.field_name_not_null: str = 'field_name should not be null'
        self.field_value_not_null: str = 'field_value should not be null'
        self.field_not_null: str = '%s should not be null'
        self.values_not_null: str = 'Values should not be null'

    def get_all(self, order_by=None) -> QuerySet:
        """
        Gets all model object list
        :return: a list of model object
        """

        self.logger.debug('Getting all %s' % self.model_name)

        try:
            model_object_list: QuerySet = self.model_class.objects.all()
            self.logger.debug('All %s got' % self.model_name)
            if order_by:
                model_object_list = model_object_list.order_by(order_by)
            return model_object_list
        except Exception as e:
            self.logger.error(e)
            raise e

    def get_by_pk(self, model_object_id):
        """
        Gets a model object by id
        :param model_object_id: the model object id
        :return: the model object
        """

        if model_object_id is None:
            error_message: str = self.id_not_null
            self.logger.error(error_message)
            raise Exception(error_message)

        self.logger.debug('Getting %s object with id %s' % (self.model_name, model_object_id))

        try:
            model_object = self.model_class.objects.get(pk=model_object_id)
            self.logger.debug('%s object with id %s got' % (self.model_name, model_object_id))
            return model_object
        except Exception as e:
            self.logger.error(e)
            raise e

    def get_by_field(self, field_name, field_value):
        """
        Gets a model object by id
        :param field_name: the model object field_name
        :param field_value: the model object field_value

        :return: the model object
        """
        if field_name is None:
            error_message = self.field_name_not_null
            self.logger.error(error_message)
            raise Exception(error_message)
        if field_value is None:
            error_message = self.field_value_not_null
            self.logger.error(error_message)
            raise Exception(error_message)

        self.logger.debug('Getting %s object with %s %s' % (self.model_name, field_name, field_value))

        try:
            query = {field_name: field_value}
            model_object = self.model_class.objects.get(**query)
            self.logger.debug('%s object with %s %s got' % (self.model_name, field_name, field_value))
            return model_object
        except Exception as e:
            self.logger.error(e)
            raise e

    def parse_contains_fields(self, search_filter, field_list=[]):
        """
        parse contains fields
        :type search_filter: dict
        :type field_list: list
        :return: search_filter: dict
        """
        try:
            if search_filter:
                for filter_name in field_list:
                    if (filter_name in search_filter) and search_filter[filter_name]:
                        search_value = search_filter.pop(filter_name, None)
                        if search_value:
                            search_filter[filter_name + '__icontains'] = search_value
            return search_filter
        except Exception as e:
            self.logger.error(e)
            raise e

    def parse_date_range_fields(self, search_filter, field_list=[], consider_equal_start=True, consider_equal_end=True):
        """
        parse date_range fields
        :type search_filter: dict
        :type field_list: list
        :return: search_filter: dict
        """
        try:
            if search_filter:
                for filter_name in field_list:
                    filter_name_start = filter_name + '_start'
                    filter_name_end = filter_name + '_end'
                    if ((filter_name_start in search_filter) and search_filter[filter_name_start]) and (
                            (filter_name_end in search_filter) and search_filter[filter_name_end]):
                        search_value_start = search_filter.pop(filter_name_start, None)
                        search_value_end = search_filter.pop(filter_name_end, None)

                        search_date_start = timezone.make_aware(
                            datetime.strptime(search_value_start, labels.DATE_FORMAT_EN))
                        search_date_end = timezone.make_aware(
                            datetime.strptime(search_value_end, labels.DATE_FORMAT_EN))
                        search_date_end = search_date_end + timezone.timedelta(days=1)

                        if consider_equal_start:
                            search_filter[filter_name + '__gte'] = search_date_start
                        else:
                            search_filter[filter_name + '__gt'] = search_date_start
                        if consider_equal_end:
                            search_filter[filter_name + '__lte'] = search_date_end
                        else:
                            search_filter[filter_name + '__lt'] = search_date_end
                    elif (filter_name_start in search_filter) and search_filter[filter_name_start]:
                        search_value_start = search_filter.pop(filter_name_start, None)
                        search_filter.pop(filter_name_end, None)

                        search_date_start = timezone.make_aware(
                            datetime.strptime(search_value_start, labels.DATE_FORMAT_EN))
                        search_date_end = timezone.make_aware(
                            datetime.strptime(search_value_start, labels.DATE_FORMAT_EN)) + timezone.timedelta(days=1)

                        search_filter[filter_name + '__gte'] = search_date_start
                        search_filter[filter_name + '__lte'] = search_date_end
            return search_filter
        except Exception as e:
            self.logger.error(e)
            raise e

    def parse_fk_fields(self, search_filter, field_list=[]):
        """
        parse contains fields
        :type search_filter: dict
        :type field_list: list
        :return: search_filter: dict
        """
        try:
            if search_filter:
                for filter_name in field_list:
                    if (filter_name in search_filter) and search_filter[filter_name]:
                        search_value = search_filter.pop(filter_name, None)
                        if search_value:
                            search_filter[filter_name + '__id'] = search_value
            return search_filter
        except Exception as e:
            self.logger.error(e)
            raise e

    def parse_like_fields(self, search_filter, field_list=[]):
        """
        parse contains fields
        :type search_filter: dict
        :type field_list: list
        :return: search_filter: dict
        """
        try:
            if search_filter:
                for filter_name in field_list:
                    if (filter_name in search_filter) and search_filter[filter_name]:
                        search_value = search_filter.pop(filter_name, None)
                        if search_value:
                            search_filter[filter_name + '__icontains'] = search_value
            return search_filter
        except Exception as e:
            self.logger.error(e)
            raise e

    def get_filtered(self, search_filter, model_object_list=None, origin_names_list=[], search_names_list=[],
                     contains_field_list=[], date_range_fields=[], fk_fields=[], keep_packed_fields=[], like_fields=[],
                     order_by='id', ascendant=True, keep_together=False):
        """
        Gets model object filtered
        :type search_filter: dict
        :type model_object_list: object
        :type origin_names_list: list
        :type search_names_list: list
        :type contains_field_list: list
        :type date_range_fields: list
        :type fk_fields: list
        :type order_by: str
        :type ascendant: bool
        :return: a list of model object filtered: list
        :keep_together: does not split search_filter values when the key ends with __in
        """
        try:
            if search_filter:
                self.logger.info('search_filter = %s' % search_filter)

                if origin_names_list and search_names_list and len(origin_names_list) == len(search_names_list):
                    for origin_name_element, search_name_element in zip(origin_names_list, search_names_list):
                        search_value = search_filter.pop(origin_name_element, None)
                        if search_value:
                            search_filter[search_name_element] = search_value

                if contains_field_list:
                    search_filter = self.parse_contains_fields(search_filter, field_list=contains_field_list)

                if date_range_fields:
                    search_filter = self.parse_date_range_fields(search_filter, field_list=date_range_fields)

                if fk_fields:
                    search_filter = self.parse_fk_fields(search_filter, field_list=fk_fields)

                if like_fields:
                    search_filter = self.parse_like_fields(search_filter, field_list=like_fields)

                search_filter_to_iterate = search_filter.copy()

                for search_element_key in search_filter_to_iterate:
                    if type(search_filter[search_element_key]) is list and len(search_filter[search_element_key]) == 1 \
                            and search_element_key not in keep_packed_fields:
                        self.logger.debug(search_element_key)
                        if search_filter[search_element_key][0] and not keep_together:
                            search_filter[search_element_key] = search_filter[search_element_key][0]
                        else:
                            search_filter.pop(search_element_key, None)
                            continue

                    if search_element_key.endswith('__in') and not type(
                            search_filter[search_element_key]) is list and not keep_together:
                        search_filter[search_element_key] = search_filter[search_element_key].split()

                    if search_filter[search_element_key] == '':
                        search_filter.pop(search_element_key, None)

                self.logger.info('search_filter parsed = %s' % search_filter)

                self.logger.debug('Getting all %s filtered' % self.model_name)
                if model_object_list is None:
                    model_object_list = self.model_class.objects.filter(**search_filter)
                else:
                    model_object_list = model_object_list.filter(**search_filter)
                self.logger.debug('All %s filtered got' % self.model_name)
            else:
                self.logger.debug('Getting all %s filtered' % self.model_name)
                if model_object_list is None:
                    model_object_list = self.get_all()
                self.logger.debug('All %s got' % self.model_name)

            model_object_list = model_object_list.distinct()
            if order_by:
                if ascendant:
                    model_object_list = model_object_list.order_by(F(order_by).asc())
                else:
                    model_object_list = model_object_list.order_by(F(order_by).desc())

            return model_object_list
        except Exception as e:
            self.logger.error(e)
            raise e

    def create(self, **kwargs):
        """
        Create a model object
        :return: the created model
        """

        self.logger.debug('Creating a %s with fields %s' % (self.model_name, kwargs))

        if kwargs is None:
            error_message = self.values_not_null
            self.logger.error(error_message)
            raise Exception(error_message)

        try:
            model_object = self.model_class.objects.create(kwargs)
            self.logger.debug('%s created a with fields %s' % (self.model_name, kwargs))
            return model_object
        except Exception as e:
            self.logger.error(e)
            raise e


def order_queryset(element_list, order_field_list, order_field_type_list=[], ascendant=True):
    logger = logging.getLogger(__name__)
    order_clause = []
    for index, order_field in enumerate(order_field_list):
        if order_field_type_list and len(order_field_type_list) >= index:
            order_field_type = order_field_type_list[index]
            if order_field_type == int:
                try:
                    logger.debug(order_field)
                    annotate_name = order_field + '_int'
                    logger.debug(annotate_name)
                    annotate_kwargs = {annotate_name: Cast(order_field, IntegerField())}
                    logger.debug(annotate_kwargs)
                    element_list = element_list.annotate(**annotate_kwargs)
                    order_field = annotate_name
                except Exception as e:
                    logger.error(e)

        if ascendant:
            order_clause.append(F(order_field).asc(nulls_last=True))
        else:
            order_clause.append(F(order_field).desc(nulls_last=True))
    return element_list.order_by(*order_clause)
