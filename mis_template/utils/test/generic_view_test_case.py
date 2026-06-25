# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
from random import choice
from string import ascii_uppercase

from django.core import serializers
from django.db.models import F
from django.urls import reverse
from django.utils.timezone import localtime

from mis_template.utils import labels
from mis_template.utils import status
from mis_template.utils.test.generic_test_case import GenericTestCase


class GenericViewTest(GenericTestCase):
    logger = logging.getLogger(__name__)

    app_admin_username = ''
    app_manager_username = ''
    app_user_username = None
    app_nonauthorized_username = 'nouser'

    all_roles_list = [app_admin_username, app_manager_username, app_nonauthorized_username]

    def setUp(self):
        self.logger.debug('#### setUp START ####')

        self.model_name = ''
        self.reference_name = ''
        self.service_class = None

        self.labels = labels

        self.is_cas_authenticated = False
        self.is_authenticated = False
        self.check_unauthorized_user = False
        self.check_authorized_user_list = []

        self.list_filter_list = [{}]
        self.list_database_query = None

        self.model_class = None
        self.form_class = None
        self.new_json_data = {}

        self.existing_object = 1
        self.not_existing_object = 9999

        self.template_directory_name = ''

        self.invalid_json_data = {'fake_attribute': 'fake_value'}
        self.create_validation = {}
        self.create_valid_json_data = {}
        self.create_excluded_validation = []

        self.mandatory_field_list = []
        self.foreignkey_field_list = []
        self.m2m_field_list = []
        self.date_field_list = []
        self.datetime_field_list = []

        self.update_validation = {}
        self.update_valid_json_data = {}
        self.update_excluded_validation = []

        self.current_local_time = localtime()  # Just to keep localtime import due to call in eval

        self.logger.debug('#### setUp END ####')

    def list(self, order_by=None, ascendant=None):
        self.logger.debug('#### TEST view %s list START ####' % self.model_name)

        url = reverse(self.reference_name + '_list')

        if self.is_cas_authenticated:
            self.logger.debug(labels.TEST_URL % url)
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET'])
        else:
            self.allowed_http_methods_testing(url, ['GET'])

        # Should return status 200 if everything goes fine
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_queryset = response.context['object_list']

        database_queryset = self.service_class.get_all()
        if self.list_database_query:
            database_queryset = database_queryset.filter(self.list_database_query)
        if order_by:
            if ascendant:
                database_queryset = database_queryset.order_by(F(order_by).asc())
            else:
                database_queryset = database_queryset.order_by(F(order_by).desc())

        if len(database_queryset) > 10:
            # Pagination case
            self.assertEqual(len(response_queryset), 10)
        else:
            self.assertEqual(len(response_queryset), len(database_queryset))
        queryset_iterator = 0
        for object_element in response_queryset:
            self.assertEqual(object_element, database_queryset[queryset_iterator])
            queryset_iterator += 1

        # Filter testing
        for filter_args in self.list_filter_list:
            arg_string = ''
            if filter_args and len(filter_args):
                first_arg = filter_args.popitem()
                arg_string = '?%s=%s' % (first_arg[0], first_arg[1])
                for arg in filter_args:
                    arg_string += '&%s=%s' % (arg, filter_args[arg])

            url = reverse(self.reference_name + '_list') + arg_string

            self.logger.debug(labels.TEST_URL % url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_queryset = response.context['object_list']
            database_queryset = self.service_class.get_filtered(filter_args)
            if len(database_queryset) > 10:
                # Pagination case
                self.assertEqual(len(response_queryset), 10)
            else:
                self.assertEqual(len(response_queryset), len(database_queryset))
            if order_by:
                if ascendant:
                    database_queryset = database_queryset.order_by(F(order_by).asc())
                else:
                    database_queryset = database_queryset.order_by(F(order_by).desc())
            queryset_iterator = 0

            for object_element in response_queryset:
                self.assertEqual(object_element, database_queryset[queryset_iterator])
                queryset_iterator += 1

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'GET')

        self.logger.debug('#### TEST view %s list END ####' % self.model_name)

    def detail(self, match_field_name=None):
        self.logger.debug('#### TEST view %s detail START ####' % self.model_name)

        url = reverse(self.reference_name + '_detail', args=[self.existing_object])

        if self.is_cas_authenticated:
            self.logger.debug(labels.TEST_URL % url)
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET'])
        else:
            self.allowed_http_methods_testing(url, ['GET'])

        # Should return status 404 for not existent object
        url = reverse(self.reference_name + '_detail', args=[self.not_existing_object])
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Should return status 200 if everything goes fine
        url = reverse(self.reference_name + '_detail', args=[self.existing_object])
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, labels.BUTTON_BACK)
        response_object = response.context['object']

        if match_field_name:
            self.assertEqual(getattr(response_object, match_field_name), self.existing_object)
        else:
            self.assertEqual(response_object.id, self.existing_object)

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'GET')

        self.logger.debug('#### TEST view %s detail END ####' % self.model_name)

    def validate_new_register(self, create_valid_json_data, object_created):
        self.logger.debug('#### TEST view %s validate new register: %s END ####' % (self.model_name, object_created))
        for key in self.create_valid_json_data.keys():
            if key in self.create_excluded_validation:
                continue
            if self.create_validation:
                if key in self.create_validation.keys():
                    if key in self.foreignkey_field_list:
                        eval('self.assertEqual(object_created.%s.id, self.create_validation[\'%s\'])' % (key, key))
                    else:
                        eval('self.assertEqual(object_created.%s, self.create_validation[\'%s\'])' % (key, key))
            else:
                if key in self.foreignkey_field_list:
                    eval('self.assertEqual(object_created.%s.id, create_valid_json_data[\'%s\'])' % (key, key))
                elif key in self.m2m_field_list:
                    eval(
                        'self.assertEqual(list(map(lambda x: x.id, object_created.%s.all())), create_valid_json_data[\'%s\'])' % (
                            key, key))
                elif key in self.date_field_list:
                    eval(
                        'self.assertEqual(object_created.%s.strftime("%%Y-%%m-%%d"), create_valid_json_data[\'%s\'])' % (
                        key, key))
                elif key in self.datetime_field_list:
                    eval(
                        'self.assertEqual(localtime(object_created.%s).strftime("%%Y-%%m-%%d %%H:%%M:%%S"), create_valid_json_data[\'%s\'])' % (
                        key, key))
                else:
                    eval('self.assertEqual(object_created.%s, create_valid_json_data[\'%s\'])' % (key, key))

    def new(self):
        self.logger.debug('#### TEST view %s create START ####' % self.model_name)

        url = reverse(self.reference_name + '_new')
        if self.is_cas_authenticated:
            self.logger.debug(labels.TEST_URL % url)
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET', 'POST', 'PUT'])
        else:
            self.allowed_http_methods_testing(url, ['GET', 'POST', 'PUT'])

        count = self.model_class.objects.count()

        # Should return status 200 if everything goes fine
        self.check_form_get_method(url, self.form_class, True)

        template_name = self.template_directory_name + 'form.html'


        self.logger.debug(labels.TEST_DATA % self.invalid_json_data)
        response = self.client.post(url, self.invalid_json_data.copy())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug(labels.TEST_RESPONSE % response)
        self.assertEqual(response.template_name[0], template_name)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)

        for mandatory_field_name in self.mandatory_field_list:
            self.create_check_mandatory_fields(url, self.create_valid_json_data.copy(), mandatory_field_name,
                                               template_name)

        self.logger.debug(labels.TEST_DATA % self.create_valid_json_data)
        response = self.client.post(url, self.create_valid_json_data.copy())
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse(self.reference_name + '_list'))

        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, count + 1)

        object_created = self.model_class.objects.last()

        self.validate_new_register(self.create_valid_json_data, object_created)

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'POST')

        self.logger.debug('#### TEST view %s create END ####' % self.model_name)

    def check_form_get_method(self, url, form_class, create=False):
        # Should return status 200 if everything goes fine
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        my_form = response.context['form']

        self.assertIsInstance(my_form, form_class)

        if create:
            self.assertFalse(my_form.instance.id)
        else:
            self.assertTrue(my_form.instance.id)

        self.assertContains(response, self.labels.BUTTON_TEXT_BACK)
        self.assertContains(response, self.labels.BUTTON_TEXT_SAVE)

        return my_form

    def create_check_mandatory_fields(self, url, json_data, mandatory_field_name, template_name):

        json_data[mandatory_field_name] = ''

        response = self.client.post(url, json_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug(labels.TEST_RESPONSE % response)
        self.assertEqual(response.template_name[0], template_name)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)
        self.assertTrue(mandatory_field_name in response.context['form'].errors)
        self.assertEqual(response.context['form'].errors[mandatory_field_name][0], self.field_required_text)

    def create_check_length_fields(self, url, json_data, field_name, template_name, max_length):

        json_data[field_name] = ''.join(choice(ascii_uppercase) for i in range(max_length + 1))

        if max_length == 1:
            error_message = self.field_length_exceeded_text % (max_length, (max_length + 1))
            error_message = error_message.replace('characters', 'character')
        else:
            error_message = self.field_length_exceeded_text % (max_length, (max_length + 1))

        response = self.client.post(url, json_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug(labels.TEST_RESPONSE % response)
        self.assertEqual(response.template_name[0], template_name)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)
        self.assertTrue(field_name in response.context['form'].errors)
        self.assertEqual(response.context['form'].errors[field_name][0], error_message)

    def update(self, match_field_name=None):
        self.logger.debug('#### TEST view %s update START ####' % self.model_name)

        url = reverse(self.reference_name + '_edit', args=[self.existing_object])
        if self.is_cas_authenticated:
            self.logger.debug(labels.TEST_URL % url)
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET', 'POST', 'PUT'])
        else:
            self.allowed_http_methods_testing(url, ['GET', 'POST', 'PUT'])

        count = self.model_class.objects.count()

        # Should return status 404 for not existent object
        url = reverse(self.reference_name + '_edit', args=[self.not_existing_object])
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Should return status 200 if everything goes fine
        url = reverse(self.reference_name + '_edit', args=[self.existing_object])
        self.check_form_get_method(url, self.form_class, False)

        template_name = self.template_directory_name + 'form.html'

        response = self.client.post(url, self.invalid_json_data.copy())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.debug(labels.TEST_RESPONSE % response)
        self.assertEqual(response.template_name[0], template_name)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)

        for mandatory_field_name in self.mandatory_field_list:
            self.create_check_mandatory_fields(url, self.update_valid_json_data.copy(), mandatory_field_name,
                                               template_name)

        response = self.client.post(url, self.update_valid_json_data.copy(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse(self.reference_name + '_list'))

        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, count)

        if match_field_name:
            query = {match_field_name: self.existing_object}
            object_updated = self.model_class.objects.self.client.get(**query)
        else:
            object_updated = self.model_class.objects.self.client.get(pk=self.existing_object)

        for key in self.update_valid_json_data.keys():
            if key in self.update_excluded_validation:
                continue
            if self.update_validation:
                if key in self.update_validation.keys():
                    if key in self.foreignkey_field_list:
                        eval('self.assertEqual(object_updated.%s.id, self.update_valid_json_data[\'%s\'])' % (key, key))
                    else:
                        eval('self.assertEqual(object_updated.%s, self.update_valid_json_data[\'%s\'])' % (key, key))
            else:
                if key in self.foreignkey_field_list:
                    eval('self.assertEqual(object_updated.%s.id, self.update_valid_json_data[\'%s\'])' % (key, key))
                elif key in self.m2m_field_list:
                    eval(
                        'self.assertEqual(list(map(lambda x: x.id, object_updated.%s.all())), self.update_valid_json_data[\'%s\'])' % (
                            key, key))
                elif key in self.date_field_list:
                    eval(
                        'self.assertEqual(object_updated.%s.strftime("%%Y-%%m-%%d"), self.update_valid_json_data[\'%s\'])' % (
                        key, key))
                elif key in self.datetime_field_list:
                    eval(
                        'self.assertEqual(localtime(object_updated.%s).strftime("%%Y-%%m-%%d %%H:%%M:%%S"), self.update_valid_json_data[\'%s\'])' % (
                        key, key))
                else:
                    eval('self.assertEqual(str(object_updated.%s), str(self.update_valid_json_data[\'%s\']))' % (
                        key, key))

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'POST')

        self.logger.debug('#### TEST view %s update END ####' % self.model_name)

    def check_delete_get_method(self, url):
        # Should return status 200 if everything goes fine
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.labels.BUTTON_TEXT_BACK)
        self.assertContains(response, self.labels.BUTTON_TEXT_CONFIRM)

        return None

    def delete(self):
        self.logger.debug('#### TEST view %s delete START ####' % self.model_name)

        url = reverse(self.reference_name + '_delete', args=[self.existing_object])
        if self.is_cas_authenticated:
            self.logger.debug(labels.TEST_URL % url)
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.is_authenticated = True

        if self.is_authenticated:
            self.login_and_check_http_methods(self.authorized_username, url, ['GET', 'POST', 'PUT', 'DELETE'])
        else:
            self.allowed_http_methods_testing(url, ['GET', 'POST', 'PUT', 'DELETE'])

        count = self.model_class.objects.count()

        # Should return status 404 for not existent object
        url = reverse(self.reference_name + '_delete', args=[self.not_existing_object])
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Should return status 200 if everything goes fine
        url = reverse(self.reference_name + '_delete', args=[self.existing_object])
        self.check_delete_get_method(url)

        template_name = self.template_directory_name + 'delete.html'

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse(self.reference_name + '_list'))

        new_count = self.model_class.objects.count()
        self.assertEqual(new_count, count - 1)

        url = reverse(self.reference_name + '_delete', args=[self.existing_object])
        self.logger.debug(labels.TEST_URL % url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        if self.check_unauthorized_user:
            self.check_roles(self.check_authorized_user_list, url, 'DELETE')

        self.logger.debug('#### TEST view %s delete END ####' % self.model_name)

    def model_formset_to_request_json(self, element_list, formset_name, field_list):
        self.logger.debug(element_list)
        serialized_model_json_list = json.loads(serializers.serialize('json', element_list))
        result_json = {formset_name + '-TOTAL_FORMS': len(serialized_model_json_list),
                       formset_name + '-INITIAL_FORMS': len(serialized_model_json_list),
                       formset_name + '-MIN_NUM_FORMS': '0', formset_name + '-MAX_NUM_FORMS': '1000'}
        for index, serialized_model_json in enumerate(serialized_model_json_list):
            prefix = '%s-%s-' % (formset_name, index)
            for key, value in serialized_model_json.items():
                if key == 'pk':
                    result_json[prefix + 'id'] = value
                if key == 'fields':
                    for fields_key, fields_value in value.items():
                        if fields_key in field_list:
                            result_json[prefix + fields_key] = fields_value
            result_json[prefix + 'DELETE'] = ''

        if serialized_model_json_list:
            last_element = len(serialized_model_json_list)
        else:
            last_element = 0
        return result_json, last_element

    def formset_to_request_json(self, formset_list, formset_name):
        self.logger.debug(formset_list)

        result_json = {formset_name + '-TOTAL_FORMS': len(formset_list),
                       formset_name + '-INITIAL_FORMS': len(formset_list), formset_name + '-MIN_NUM_FORMS': '0',
                       formset_name + '-MAX_NUM_FORMS': '1000'}

        for index, formset in enumerate(formset_list):
            prefix = '%s-%s-' % (formset_name, index)
            if formset:
                for key, value in formset.data():
                    if key == 'pk':
                        result_json[prefix + 'id'] = value
                    if key == 'fields':
                        for fields_key, fields_value in value.items():
                            result_json[prefix + fields_key] = fields_value
                result_json[prefix + 'DELETE'] = ''

        if formset_list:
            last_element = len(formset_list)
        else:
            last_element = 0
        return result_json, last_element
